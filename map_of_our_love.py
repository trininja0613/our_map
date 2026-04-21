import folium
from folium.plugins import AntPath
import math
import requests 
import time
from datetime import datetime
import pytz

# --- Configuration ---
API_KEY = "a288bd9e5aa8fa7b28430f8ce42032b4"
my_house = [35.294115873209485, -80.68320214758597]
her_house = [42.492732322838044, -92.34678268757763]
midpoint = [(my_house[0] + her_house[0]) / 2, (my_house[1] + her_house[1]) / 2]

# --- Logic Functions ---
def get_local_times():
    clt_tz, alo_tz = pytz.timezone('US/Eastern'), pytz.timezone('US/Central')
    clt_time = datetime.now(clt_tz).strftime('%I:%M %p')
    alo_time = datetime.now(alo_tz).strftime('%I:%M %p')
    return clt_time, alo_time

def get_weather(lat, lon):
    # Professional Retry Loop (tries 3 times)
    for attempt in range(3):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return f"{data['main']['temp']:.0f}°F, {data['weather'][0]['description']}"
        except Exception:
            time.sleep(2) # Wait 2 seconds before retrying
    return "Weather Offline"

def calculate_haversine(coord1, coord2):
    R = 3958.8
    lat1, lon1, lat2, lon2 = map(math.radians, [coord1[0], coord1[1], coord2[0], coord2[1]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

# --- Execute Logic ---
clt_tz = pytz.timezone('US/Eastern')
clt_now, alo_now = get_local_times()
clt_weather = get_weather(my_house[0], my_house[1])
alo_weather = get_weather(her_house[0], her_house[1])
exact_miles = calculate_haversine(my_house, her_house)
last_heartbeat = datetime.now(clt_tz).strftime('%b %d, %I:%M %p')

# Distance Math
drive_time = exact_miles / 65 
flight_time = 2.5 

# --- Countdown Transition Logic ---
target_date = datetime(2026, 5, 7, 12, 0, 0, tzinfo=clt_tz)
now = datetime.now(clt_tz)
days_until = (target_date - now).days

if days_until > 1:
    countdown_text = f"<b>{days_until} Days</b> until Charlotte ❤️"
elif days_until == 1:
    countdown_text = "<b>Tomorrow!</b> ✈️"
elif 0 >= days_until >= -7:
    countdown_text = "<b>Reign is in Charlotte!</b> ✨"
else:
    countdown_text = "<b>Connection Strong</b> ❤️"

# --- Map Construction ---
m = folium.Map(location=[38.5, -86.5], zoom_start=6, tiles="Cartodb dark_matter")

dashboard_html = f"""
<style>
    .connection-box {{
        position: fixed; top: 15px; right: 15px; width: 250px;
        background-color: rgba(255, 255, 255, 0.9); border: 2px solid #FF0000;
        z-index: 9999; border-radius: 12px; padding: 12px;
        font-family: 'Segoe UI', sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .countdown-banner {{
        background: linear-gradient(45deg, #8B0000, #FF0000);
        color: white; padding: 5px; border-radius: 6px;
        text-align: center; margin-bottom: 8px; font-size: 13px;
    }}
    .sync-text {{ font-size: 9px; color: #666; margin-top: 8px; text-align: center; }}
    @media only screen and (max-width: 600px) {{
        .connection-box {{ width: 180px; padding: 8px; }}
        .connection-box b, .connection-box span {{ font-size: 10px; }}
    }}
</style>

<div class="connection-box">
    <div class="countdown-banner">{countdown_text}</div>
    <center><b style="color: #8B0000;">Connection Status</b></center>
    <hr style="border: 0.5px solid #ccc; margin: 5px 0;">
    <div>
        <b>Waterloo:</b> <span id="alo-clock">Syncing...</span> • <span>{alo_weather}</span><br>
        <b>Charlotte:</b> <span id="clt-clock">Syncing...</span> • <span>{clt_weather}</span><br>
        <b>Gap:</b> <span>{exact_miles:.0f} miles</span><br>
        <b>Travel:</b> <span>~{drive_time:.0f}h Drive / {flight_time}h Flight</span>
    </div>
    <div class="sync-text">Last Heartbeat: {last_heartbeat} ET</div>
</div>
"""
m.get_root().html.add_child(folium.Element(dashboard_html), name="dashboard")

# Heartbeat Pulse
AntPath(locations=[my_house, her_house], color="#FF0000", pulse_color="#FFFFFF", 
        weight=5, delay=800, dash_array=[15, 30]).add_to(m)

# Midpoint Icon
folium.Marker(midpoint, icon=folium.DivIcon(html='<div style="font-size: 30px; filter: drop-shadow(0 0 5px gold);">☀️</div>')).add_to(m)

# Home/Heart Markers
folium.Marker(my_house, popup="My House", icon=folium.Icon(color='blue', icon='home')).add_to(m)
folium.Marker(her_house, popup="Her House", icon=folium.Icon(color='red', icon='heart')).add_to(m)

# Secret Message
live_clock_script = """
<script>
function updateClocks() {
    const options = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    
    // Waterloo is Central Time
    document.getElementById('alo-clock').innerHTML = new Date().toLocaleTimeString('en-US', {
        ...options, timeZone: 'America/Chicago'
    });
    
    // Charlotte is Eastern Time
    document.getElementById('clt-clock').innerHTML = new Date().toLocaleTimeString('en-US', {
        ...options, timeZone: 'America/New_York'
    });
}

function showSecret() {
    alert("I created this code because you are my muse. You influence everything I create. I love you so much, you mean the world to me. No matter the distance, I feel connected to you. This string pulses at the speed of my heart whenever I'm thinking of you. Mahal Kita, Reign! ❤️");
}

// Update every second
setInterval(updateClocks, 1000);
updateClocks(); // Initial call
</script>
<button onclick="showSecret()" style="position:fixed; bottom:30px; left:30px; z-index:9999; 
    padding:12px 24px; background:linear-gradient(45deg, #8B0000, #FF0000); color:white; 
    border-radius:30px; border:none; cursor:pointer; font-weight:bold; box-shadow: 0 4px 15px rgba(255,0,0,0.5);">
    A Message for Reign
</button>
"""
m.get_root().html.add_child(folium.Element(dashboard_html), name="dashboard")
m.get_root().html.add_child(folium.Element(live_clock_script))
m.get_root().header.add_child(folium.Element('<meta name="viewport" content="width=device-width, initial-scale=1.0">'))

m.save("index.html")
print(f"Map updated at {last_heartbeat}")