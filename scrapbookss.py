import datetime
import tkinter as tk
from PIL import Image, ImageTk
import glob
import os
import re
import random

# --- COLOR PALETTE ---
COLOR_FOREST_GREEN = "#228B22"
COLOR_PLUM = "#8E4585"
COLOR_LIGHT_PINK = "#FFB6C1"
COLOR_TEXT_ON_DARK = "#FFFFFF"

#---THEMES---#
THEMES = [
    {
        "name": "Forest Romance",
        "bg": "#228B22", "btn": "#FFB6C1", "txt": "#FFFFFF", "accent": "#8E4585"
    },
    {
        "name": "Sunrise Bliss",
        "bg": "#FF7E5F", "btn": "#FEB47B", "txt": "#FFFFFF", "accent": "#6A0572"
    },
    {
        "name": "Full Moon Magic",
        "bg": "#2C3E50", "btn": "#95A5A6", "txt": "#ECF0F1", "accent": "#34495E"
    },
    {
        "name": "Starry Sky",
        "bg": "#0B1026", "btn": "#333333", "txt": "FFFFFF", "accent": "#FF0000"
    },
    {
        "name": "Red Line Theory",
        "bg": "#8B0000", "btn": "#333333", "txt": "#FFFFFF", "accent": "#FF0000"
    },
    {
        "name": "Beach", 
        "bg": "#0077BE", "btn": "#F4A460", "txt": "#FFFFFF", "accent": "#E1AD01"
    },
    {
        "name": "Filipina Heritage", 
        "bg": "#0038A8", "btn": "#CE1126", "txt": "#FFFFFF", "accent": "#FCD116"
    }
]

class DigitalScrapBook:
    def load_captions(self):
        caption_map = {}
        if os.path.exists("captions.txt"):
            with open("captions.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "|" in line:
                        filename, caption = line.strip().split("|", 1)
                        caption_map[filename] = caption
        return caption_map
    
    def show_splash(self):
        # Create a new pop-up window
        splash = tk.Toplevel(self.root)
        splash.title("A Message for You")
        splash.geometry("500x350")
        
        # Remove window borders for a sleek look
        splash.overrideredirect(True)
        
        # Center the splash screen on the screen
        screen_width = splash.winfo_screenwidth()
        screen_height = splash.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (350 // 2)
        splash.geometry(f"500x350+{x}+{y}")
        
        # FILIPINA THEME COLORS
        PH_BLUE = "#0038A8"
        PH_RED = "#CE1126"
        PH_YELLOW = "#FCD116"

        # Create a border frame for that "Sun" glow
        border_frame = tk.Frame(splash, bg=PH_YELLOW, padx=5, pady=5)
        border_frame.pack(expand=True, fill="both")

        # Inner content box
        content_box = tk.Frame(border_frame, bg=PH_BLUE)
        content_box.pack(expand=True, fill="both")
        
        # The main message
        tk.Label(
            content_box, 
            text="Mahal Kita <333", 
            font=("Lucida Handwriting", 28, "bold"),
            bg=PH_BLUE,
            fg=PH_YELLOW
        ).pack(expand=True, pady=(40, 10))

        # A small sub-text in Red
        tk.Label(
            content_box,
            text="Para sa iyo...", 
            font=("Lucida Handwriting", 14, "italic"),
            bg=PH_BLUE,
            fg=PH_RED
        ).pack(pady=(0, 40))
        
        # 3.5 seconds gives her just a bit more time to appreciate the colors
        self.root.after(3500, splash.destroy)
        
        # Add your message
        tk.Label(
            splash, 
            text="Mahal Kita <333", 
            font=("Lucida Handwriting", 24, "bold"),
            bg=COLOR_PLUM,
            fg=COLOR_TEXT_ON_DARK
        ).pack(expand=True)
        
        # Show for 3000ms (3 seconds) then destroy the splash window
        self.root.after(3000, splash.destroy)
    
    def __init__(self, root):
        self.root = root
        # Hide the main window while the splash shows
        self.root.withdraw() 
        self.show_splash()
        
        # Bring the main window back after the splash is gone
        self.root.after(3500, self.root.deiconify)
        self.root.title("Digital Scrapbook")
        # Standard laptop friendly height
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_FOREST_GREEN)
        
        try:
            self.root.iconbitmap("icon.ico")
        except:
            # If the icon file is missing or cannot be loaded, we can ignore the error and continue without setting an icon.
            pass
        
        # 1. LOAD ASSETS
        extensions = ("*.jpg", "*.jpeg", "*.png", "*.gif", "*.JPG", "*.JPEG", "*.PNG", "*.GIF")
        self.photo_files = []
        for ext in extensions:
            self.photo_files.extend(glob.glob(os.path.join("pictures", ext)))
        
        self.photo_files = list(set(self.photo_files)) # Remove Windows duplicates
        self.photo_files.sort(key=lambda f: [int(c) if c.isdigit() else c.lower() for c in re.split("([0-9]+)", f)])
        
        captions = self.load_captions()
        self.memories = [{"file": f, "caption": captions.get(os.path.basename(f), "A special memory...")} for f in self.photo_files]
        self.index = 0
        self.slideshow_running = False # State tracker
        
        #The Easter Egg
        self.keystrokes = ""
        #Listen for any key press on the main window
        self.root.bind("<Key>", self.check_secret_code)

        # 2. UI ELEMENTS (Compressed for vertical space)
        
        # Progress (Top)
        self.progress_label = tk.Label(self.root, text="", font=("Lucida Handwriting", 11, "italic"), bg=COLOR_FOREST_GREEN, fg=COLOR_LIGHT_PINK)
        self.progress_label.pack(pady=(5, 2))
        self.current_theme_index = 0 # Start with first theme
        
        # Falling Hearts Animation Setup
        self.hearts = []
        self.animation_running = False
       
        
        # Image (Shrunk to 300 height to save space)
        self.image_label = tk.Label(self.root, bg="white", padx=5, pady=5, highlightthickness=2, highlightbackground="#d3d3d3")
        self.image_label.pack(pady=5)
        
        # Caption
        self.caption_label = tk.Label(self.root, text="", font=("Lucida Handwriting", 12), bg=COLOR_PLUM, fg=COLOR_TEXT_ON_DARK, wraplength=500, justify="center", pady=10, padx=20, borderwidth=2, relief="ridge")
        self.caption_label.pack(pady=5)
        
        # Nav Buttons Frame
        self.button_frame = tk.Frame(self.root, bg=COLOR_FOREST_GREEN)
        self.button_frame.pack(pady=5)
        
        self.prev_button = tk.Button(self.button_frame, text="<-- Previous", command=self.show_prev, font=("Lucida Handwriting", 10, "bold"), bg=COLOR_LIGHT_PINK, fg=COLOR_PLUM, cursor="heart", padx=10)
        self.prev_button.pack(side="left", padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next -->", command=self.show_next, font=("Lucida Handwriting", 10, "bold"), bg=COLOR_LIGHT_PINK, fg=COLOR_PLUM, cursor="heart", padx=10)
        self.next_button.pack(side="left", padx=10)

        # Slideshow Button (Directly under nav)
        self.play_button = tk.Button(self.root, text="Start Slideshow ▶", command=self.toggle_slideshow, font=("Lucida Handwriting", 10, "bold"), bg=COLOR_LIGHT_PINK, fg=COLOR_PLUM, cursor="heart", padx=20)
        self.play_button.pack(pady=5)
        
        self.theme_button = tk.Button(self.root, text="Change Theme 🎨", command=self.change_theme, font=("Lucida Handwriting", 10, "bold"), bg=COLOR_LIGHT_PINK, fg=COLOR_PLUM, cursor="heart", padx=20)
        self.theme_button.pack(pady=5)

        # Jump To Section (Bottom)
        self.jump_frame = tk.Frame(self.root, bg=COLOR_FOREST_GREEN)
        self.jump_frame.pack(pady=15)
        #Assign the label to the variable FIRST, then pack it
        self.jump_to_label = tk.Label(
            self.jump_frame, 
            text="Jump to:", 
            font=("Lucida Handwriting", 10), 
            bg=COLOR_FOREST_GREEN, 
            fg=COLOR_TEXT_ON_DARK
        )
        # Now that it's defined, we can pack it
        self.jump_to_label.pack(side="left")
        
        tk.Label(self.jump_frame, text="Jump to:", font=("Lucida Handwriting", 10), bg=COLOR_FOREST_GREEN, fg=COLOR_TEXT_ON_DARK)
        self.jump_entry = tk.Entry(self.jump_frame, width=5, font=("Lucida Handwriting", 9), justify="center")
        self.jump_entry.pack(side="left", padx=5)
        self.go_button = tk.Button(self.jump_frame, text="Go", command=self.jump_to_photo, font=("Lucida Handwriting", 9, "bold"), bg=COLOR_PLUM, fg=COLOR_TEXT_ON_DARK)
        self.go_button.pack(side="left")

        # 3. BIND HOVER EFFECTS
        for btn in [self.next_button, self.prev_button, self.play_button, self.go_button]:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

        self.update_display()

    # --- METHODS ---

    def update_display(self):
        if not self.memories: return
        try:
            img_path = self.memories[self.index]["file"]
            raw_img = Image.open(img_path).convert("RGBA")
            # Shrinking max height to 300 to keep UI on screen
            raw_img.thumbnail((500, 300)) 
            self.photo = ImageTk.PhotoImage(raw_img)
            self.image_label.config(image=self.photo)
            self.caption_label.config(text=self.memories[self.index]["caption"])
            self.progress_label.config(text=f"Memory {self.index + 1} of {len(self.memories)}")
        except Exception as e:
            print(f"Error: {e}")

    def toggle_slideshow(self):
        self.slideshow_running = not self.slideshow_running
        if self.slideshow_running:
            self.play_button.config(text="Pause Slideshow ⏸", bg="#FF69B4")
            self.run_slideshow()
        else:
            self.play_button.config(text="Start Slideshow ▶", bg=COLOR_LIGHT_PINK)

    def run_slideshow(self):
        if self.slideshow_running:
            self.show_next()
            self.root.after(4000, self.run_slideshow)

    def on_enter(self, e):
        e.widget['background'] = COLOR_PLUM
        e.widget['foreground'] = COLOR_TEXT_ON_DARK

    def on_leave(self, e):
        theme = THEMES[self.current_theme_index]
        if e.widget == self.play_button and self.slideshow_running:
            e.widget['background'] = "#FF69B4" # Keep the "Active" pink
        else:
            e.widget['background'] = theme["btn"] # Match the current theme
            e.widget['foreground'] = theme["bg"]  # Match the current theme

    def jump_to_photo(self):
        try:
            target = int(self.jump_entry.get())
            if 1 <= target <= len(self.memories):
                self.index = target - 1
                self.update_display()
                self.jump_entry.delete(0, tk.END)
        except: self.jump_entry.delete(0, tk.END)

    def show_next(self):
        self.index = (self.index + 1) % len(self.memories)
        self.update_display()

    def show_prev(self):
        self.index = (self.index - 1) % len(self.memories)
        self.update_display()
        
    def change_theme(self): 
        try:
            # 1. Move the index forward
            self.current_theme_index = (self.current_theme_index + 1) % len(THEMES)
            theme = THEMES[self.current_theme_index]
            
            # 2. Update Main Window & Frames
            self.root.configure(bg=theme["bg"])
            self.button_frame.configure(bg=theme["bg"])
            self.jump_frame.configure(bg=theme["bg"])
            
            # 3. Update Text Labels
            self.progress_label.configure(bg=theme["bg"], fg=theme["btn"])
            self.jump_to_label.configure(bg=theme["bg"], fg=theme["txt"])
            self.caption_label.configure(bg=theme["accent"], fg=theme["txt"])
            
            # 4. Update Entry Box
            self.jump_entry.configure(bg=theme["accent"], fg=theme["txt"], insertbackground=theme["txt"])
            
            # 5. Handle the Theme Button Text
            self.theme_button.config(text=f"Vibe: {theme['name']} ✨", bg=theme["btn"])
            
            # 6. Handle the Slideshow Button (Theme-Aware)
            if self.slideshow_running:
                self.play_button.config(text="Pause Slideshow ⏸", bg="#FF69B4")
            else:
                self.play_button.config(text="Start Slideshow ▶", bg=theme["btn"])

            # 7. Update all other Buttons
            self.prev_button.config(bg=theme["btn"])
            self.next_button.config(bg=theme["btn"])
            self.go_button.config(bg=theme["btn"], fg=theme["bg"])

            # 8. THE RED LINE LOGIC (Simplified to prevent crashing)
            if theme["name"] == "Red Line Theory":
                if not hasattr(self, 'red_line_widget'):
                    self.red_line_widget = tk.Frame(self.root, height=3, bg="red")
                    self.red_line_widget.pack(fill="x", pady=5)
            else:
                if hasattr(self, 'red_line_widget'):
                    self.red_line_widget.destroy()
                    del self.red_line_widget

        except Exception as e:
            print(f"Theme Error: {e}") # This will tell us exactly what's wrong in the terminal
            
    def start_heart_animation(self, canvas):
        self.animation_running = True
        self.hearts = []
        
        # Give the window a millisecond to figure out its actual size
        canvas.update_idletasks()
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        for _ in range(35): # Bumped to 35 to fill larger screens better
            # Use the dynamic width/height for initial placement
            x = random.randint(0, width)
            y = random.randint(-height, 0)
            size = random.randint(12, 26)
            char = random.choice(["❤️", "❤️", "—"])
            heart_id = canvas.create_text(
                x, y, text=char, font=("Arial", size), fill="#FF0000"
            )
            self.hearts.append([heart_id, random.randint(3, 8)])
        
        self.run_animation(canvas)

    def run_animation(self, canvas):
        if not self.animation_running:
            return

        # The Secret Sauce: Get the CURRENT size of the window every frame
        win_w = canvas.winfo_width()
        win_h = canvas.winfo_height()

        for heart in self.hearts:
            canvas.move(heart[0], 0, heart[1])
            
            # Check if heart passed the CURRENT bottom of the window
            if canvas.coords(heart[0])[1] > win_h:
                # Reset to a random X within the CURRENT width
                canvas.coords(heart[0], random.randint(0, win_w), -20)
        
        self.root.after(50, lambda: self.run_animation(canvas))

    def run_animation(self, canvas):
        if not self.animation_running:
            return

        for heart in self.hearts:
            canvas.move(heart[0], 0, heart[1])
            # Reset heart to top if it falls off the bottom (650px)
            if canvas.coords(heart[0])[1] > 650:
                canvas.coords(heart[0], random.randint(0, 600), -20)
        
        # 50ms delay for smooth 20FPS animation
        self.root.after(50, lambda: self.run_animation(canvas))
        
    def check_secret_code(self, event):
        
        if event.char:
            self.keystrokes += event.char.lower()
            
            self.keystrokes = self.keystrokes[-10:]
            
            
            if "mahal kita" in self.keystrokes:
                self.keystrokes = "" # Reset after activation
                self.show_letter() 
                
    def check_secret_code(self, event):
        if event.char:
            self.keystrokes += event.char.lower()
            # Increased to 20 for extra "breathing room" in case of typos
            self.keystrokes = self.keystrokes[-20:]
            
            if "mahal kita" in self.keystrokes:
                self.keystrokes = "" 
                self.show_letter() 

    def show_letter(self):
        self.secret_win = tk.Toplevel(self.root)
        self.secret_win.title("A Secret Message")
        self.secret_win.geometry("600x650")
        self.secret_win.configure(bg="#FFF8E7")
        
        # FIXED: Use 'secret_win' instead of 'center_win'
        self.secret_win.update_idletasks()
        x = (self.secret_win.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.secret_win.winfo_screenheight() // 2) - (650 // 2)
        self.secret_win.geometry(f"+{x}+{y}")
        
        letter_text = (
            "My Dearest Reign,\n\n"
            "From the moment you entered my life, everything changed for the better. "
            "Your smile lights up my darkest days, and your laughter is the sweetest "
            "melody to my ears. I am endlessly grateful for every moment we share together.\n\n"
            "You are not just my love, but also my best friend, my confidant, and my greatest support. "
            "I cherish every memory we've created and look forward to a future filled with even more love and happiness.\n\n"
            "Mahal kita ng buong puso ko, at I promise to always be there for you, "
            "through thick and thin. You are my forever and always.\n\n"
            "With all my love,\nBrandon King"
        )
        
        tk.Label(
            self.secret_win, 
            text=letter_text, 
            font=("Lucida Handwriting", 14), 
            bg="#FFF8E7", 
            fg="#333333", 
            wraplength=500, 
            justify="left",
            padx=30,
            pady=30
        ).pack(expand=True)
        
        tk.Button(
            self.secret_win,
            text="Turn the page... 📖",
            command=self.show_proposal,
            font=("Lucida Handwriting", 12, "bold"),
            bg=COLOR_LIGHT_PINK,
            fg=COLOR_PLUM,
            cursor="heart",
            padx=15,
            pady=5
        ).pack(pady=30)
        
    def show_proposal(self):
        for widget in self.secret_win.winfo_children():
            widget.destroy()
            
        # Red String Theory Palette
        RS_BG = "#8B0000"     # Deep Crimson
        RS_BTN = "#1A1A1A"    # Sleek Near-Black
        RS_STRING = "#FF0000" # Bright Red String
        RS_TEXT = "#FFFFFF"   # Pure White

        self.secret_win.configure(bg=RS_BG)
        
        tk.Label(
            self.secret_win,
            text="I have one final question for you...",
            font=("Lucida Handwriting", 16, "bold"),
            bg=RS_BG,
            fg=RS_TEXT,
        ).pack(pady=(150, 20))
        
        tk.Label(
            self.secret_win,
            text="Will you officially be my girlfriend, Reign?",
            font=("Lucida Handwriting", 20, "bold"),
            bg=RS_BG,
            fg=RS_STRING, # The "Red String" highlight
            wraplength=500
        ).pack(pady=10)
        
        # YES BUTTON: Centered at 40% width
        self.yes_btn = tk.Button(
            self.secret_win, 
            text="Yes! 💖", 
            command=self.celebrate_yes, 
            font=("Lucida Handwriting", 14, "bold"), 
            bg=RS_BTN, 
            fg=RS_STRING, # Red text on black for that Red String look
            activebackground=RS_STRING,
            activeforeground=RS_TEXT,
            width=10,
            cursor="heart"
        )
        self.yes_btn.place(relx=0.35, rely=0.65, anchor="center")
        
        # NO BUTTON: Centered at 60% width
        self.no_btn = tk.Button(
            self.secret_win, 
            text="No", 
            font=("Lucida Handwriting", 14, "bold"), 
            bg=RS_BTN, 
            fg=RS_TEXT, 
            width=10
        )
        self.no_btn.place(relx=0.65, rely=0.65, anchor="center")
        
        self.no_btn.bind("<Enter>", self.dodge_mouse)
        
    def dodge_mouse(self, event):
        # Generates a random position between 10% and 90% of the window
        # This ensures it stays visible but is impossible to catch
        new_relx = random.uniform(0.1, 0.9)
        new_rely = random.uniform(0.4, 0.9) # Keeps it in the bottom half
        self.no_btn.place(relx=new_relx, rely=new_rely, anchor="center")
        
    def celebrate_yes(self):
        for widget in self.secret_win.winfo_children():
            widget.destroy()
            
        # Red String Final Palette
        RS_BG = "#1A1A1A"
        RS_STRING = "#FF0000"
        RS_TEXT = "#FFFFFF"
        self.secret_win.configure(bg=RS_BG)

        # 1. Create Canvas for Heart Animation
        self.cv = tk.Canvas(self.secret_win, bg=RS_BG, highlightthickness=0)
        self.cv.place(relwidth=1, relheight=1)
        self.start_heart_animation(self.cv)

        # 2. Add Content Over the Canvas
        content_frame = tk.Frame(self.secret_win, bg=RS_BG)
        content_frame.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            content_frame,
            text="I'm the luckiest guy in the world.\n\nMahal Kita, Reign. ❤️",
            font=("Lucida Handwriting", 20, "bold"),
            bg=RS_BG, fg=RS_TEXT, justify="center"
        ).pack(pady=20)

        # 3. Signature Section
        tk.Label(
            content_frame, text="Leave a note for our future selves:",
            font=("Georgia", 10, "italic"), bg=RS_BG, fg=RS_STRING
        ).pack(pady=(20, 5))

        self.signature_entry = tk.Entry(
            content_frame, font=("Georgia", 12), width=30,
            bg="#333333", fg=RS_TEXT, insertbackground=RS_STRING, bd=0
        )
        self.signature_entry.pack(pady=5, ipady=5)

        self.save_btn = tk.Button(
            content_frame, text="Seal the Promise 🖋️",
            command=self.save_response,
            font=("Georgia", 10, "bold"),
            bg=RS_STRING, fg=RS_TEXT, activebackground="#8B0000",
            cursor="heart", bd=0, padx=10, pady=5
        )
        self.save_btn.pack(pady=15)

        # 4. Back Button
        tk.Button(
            self.secret_win, text="Back to our memories",
            command=lambda: [setattr(self, 'animation_running', False), self.secret_win.destroy()],
            font=("Georgia", 9, "italic"), bg=RS_BG, fg="#555555",
            bd=0, activebackground=RS_BG, cursor="heart"
        ).pack(side="bottom", pady=10)
    
    def save_response(self):
        response_text = self.signature_entry.get()
        if response_text.strip():
            try:
                with open("response.txt", "a", encoding="utf-8") as f:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] Reign: {response_text}\n")
                
                # Visual confirmation
                self.save_btn.config(text="Saved! ❤️", state="disabled", bg="#333333")
                self.signature_entry.config(state="disabled")
            except Exception as e:
                print(f"Error saving log: {e}")
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalScrapBook(root)
    root.mainloop()