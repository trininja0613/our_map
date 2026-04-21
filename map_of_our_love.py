import folium
from folium.plugins import AntPath
import math
import requests  
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
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['main']['temp']:.0f}°F, {data['weather'][0]['description']}"
        return "Syncing..."
    except:
        return "Offline"

def calculate_haversine(coord1, coord2):
    R = 3958.8
    lat1, lon1, lat2, lon2 = map(math.radians, [coord1[0], coord1[1], coord2[0], coord2[1]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

# --- Execute Logic ---
clt_now, alo_now = get_local_times()
clt_weather = get_weather(my_house[0], my_house[1])
alo_weather = get_weather(her_house[0], her_house[1])
exact_miles = calculate_haversine(my_house, her_house)

# 3. Distance Math (Drive vs Flight)
drive_time = exact_miles / 65 # Average MPH
flight_time = 2.5 # Estimated flight hours

# --- Map Construction ---
m = folium.Map(location=[38.5, -86.5], zoom_start=6, tiles="Cartodb dark_matter")

# 1. The Dashboard (Now with Travel Math)
# --- Countdown Logic ---
from datetime import datetime
target_date = datetime(2026, 5, 7, 12, 0, 0, tzinfo=pytz.timezone('US/Eastern'))
now = datetime.now(pytz.timezone('US/Eastern'))
days_until = (target_date - now).days

# If she's already arrived or it's the day of
if days_until > 0:
    countdown_text = f"<b>{days_until} Days</b> until Charlotte ❤️"
else:
    countdown_text = "<b>The wait is over!</b> ✈️"

# --- Map Construction ---
dashboard_html = f"""
<style>
    .connection-box {{
        position: fixed; 
        top: 15px; 
        right: 15px; 
        width: 250px;
        background-color: rgba(255, 255, 255, 0.9); 
        border: 2px solid #FF0000;
        z-index: 9999; 
        border-radius: 12px; 
        padding: 12px;
        font-family: 'Segoe UI', sans-serif; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .countdown-banner {{
        background: linear-gradient(45deg, #8B0000, #FF0000);
        color: white;
        padding: 5px;
        border-radius: 6px;
        text-align: center;
        margin-bottom: 8px;
        font-size: 13px;
    }}
    @media only screen and (max-width: 600px) {{
        .connection-box {{ width: 180px; padding: 8px; top: 10px; right: 10px; }}
        .connection-box b {{ font-size: 11px; }}
        .connection-box span, .connection-box div {{ font-size: 10px; }}
        .connection-title {{ font-size: 12px !important; }}
        .countdown-banner {{ font-size: 10px; padding: 3px; }}
        .connection-quote {{ display: none; }}
    }}
</style>

<div class="connection-box">
    <div class="countdown-banner">{countdown_text}</div>
    <center><b class="connection-title" style="color: #8B0000; font-size: 14px;">Connection Status</b></center>
    <hr style="border: 0.5px solid #ccc; margin: 5px 0;">
    <div>
        <b>Waterloo:</b> <span>{alo_now} • {alo_weather}</span><br>
        <b>Charlotte:</b> <span>{clt_now} • {clt_weather}</span><br>
        <b>Gap:</b> <span>{exact_miles:.0f} miles</span><br>
        <b>Travel:</b> <span>~{drive_time:.0f}h Drive / {flight_time}h Flight</span>
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(dashboard_html))

# 5. Heartbeat Pulse (Delay=800ms is roughly 75BPM)
AntPath(
    locations=[my_house, her_house],
    color="#FF0000",
    pulse_color="#FFFFFF",
    weight=5,
    delay=800, 
    dash_array=[15, 30]
).add_to(m)

# 2. Filipino Sun / Midpoint Icon
# Using a ☀️ emoji inside a DivIcon for a custom look
folium.Marker(
    midpoint,
    popup="The warmth that bridges the distance.",
    icon=folium.DivIcon(html='''<div style="font-size: 30px; filter: drop-shadow(0 0 5px gold);">☀️</div>''')
).add_to(m)

# Markers
folium.Marker(my_house, popup="My House", icon=folium.Icon(color='blue', icon='home')).add_to(m)
folium.Marker(her_house, popup="Her House", icon=folium.Icon(color='red', icon='heart')).add_to(m)

# Secret Button
script = """
<script>
function showSecret() {
    alert("I created this code because you are my muse. You influence everything I create. I love you so much, you mean the world to me. No matter the distance, I feel connected to you. This string pulses at the speed of my heart whenever I'm thinking of you. Mahal Kita, Reign! ❤️");
}
</script>
<button onclick="showSecret()" style="position:fixed; bottom:30px; left:30px; z-index:9999; 
    padding:12px 24px; background:linear-gradient(45deg, #8B0000, #FF0000); color:white; 
    border-radius:30px; border:none; cursor:pointer; font-weight:bold; box-shadow: 0 4px 15px rgba(255,0,0,0.5);">
    A Message for Reign
</button>
"""
m.get_root().html.add_child(folium.Element(script))

# This ensures the map scales perfectly on Reign's iPhone/Android
m.get_root().header.add_child(folium.Element('<meta name="viewport" content="width=device-width, initial-scale=1.0">'))

m.save("index.html")
print("The Ultimate Connection Map is ready!")