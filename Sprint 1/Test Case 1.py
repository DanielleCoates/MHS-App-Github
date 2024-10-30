# TC01 Script
# 10-30-2024


import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Define mood scale
MOOD_SCALE = {
    "Very Sad": 1,
    "Sad": 2,
    "Okay": 3,
    "Slightly Happy": 4,
    "Happy": 5,
    "Very Happy": 6,
}

stored_username = "admin"
stored_password = "password123"

# Initialize main app window
root = tk.Tk()
root.title("MHS: Mental Health Support App")
root.geometry("400x300")
root.configure(bg="#F5F5F5")  # Light background for a clean look

# Set a custom font style
custom_font = ("Helvetica", 12, "bold")

# URL of the logo image online
logo_url = "https://www.dubaicosmeticsurgery.com/wp-content/uploads/2023/06/mental.png" 

# Global variables for entry fields and label
login_frame = None
permission_frame = None
main_frame = None
mood_entry = None
note_entry = None

# Function to show the main login screen
def show_login_screen():
    global login_frame
    login_frame = tk.Frame(root, bg="#F5F5F5")
    login_frame.pack(pady=20)

    # Display logo and title
    try:
        response = requests.get(logo_url)  # Fetch image from the URL
        response.raise_for_status()  # Check for errors
        logo = Image.open(BytesIO(response.content))
        logo = logo.resize((50, 50), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(login_frame, image=logo_img, bg="#F5F5F5")
        logo_label.image = logo_img  # Keep a reference to prevent garbage collection
        logo_label.grid(row=0, column=0, rowspan=2, padx=10)
    except requests.exceptions.RequestException as e:
        print("Failed to load logo image:", e)

    # App title
    title_label = tk.Label(login_frame, text="MHS: Mental Health Support App", font=("Helvetica", 16, "bold"), bg="#F5F5F5", fg="#333333")
    title_label.grid(row=0, column=1, columnspan=2, pady=(10, 20))

    # Username label and entry
    tk.Label(login_frame, text="Username:", font=custom_font, bg="#F5F5F5").grid(row=1, column=0, sticky="e")
    username_entry = tk.Entry(login_frame, width=25, font=("Helvetica", 12))
    username_entry.grid(row=1, column=1, columnspan=2, pady=5)

    # Password label and entry
    tk.Label(login_frame, text="Password:", font=custom_font, bg="#F5F5F5").grid(row=2, column=0, sticky="e")
    password_entry = tk.Entry(login_frame, width=25, font=("Helvetica", 12), show="*")
    password_entry.grid(row=2, column=1, columnspan=2, pady=5)

    # Error message placeholder
    error_message = tk.Label(login_frame, text="", fg="red", bg="#F5F5F5", font=("Helvetica", 10, "italic"))
    error_message.grid(row=3, column=0, columnspan=3, pady=5)

    # Verification function for login
    def verify_login():
        if username_entry.get() == stored_username and password_entry.get() == stored_password:
            error_message.config(text="")
            login_frame.pack_forget()
            show_permission_screen()  # Navigate to the next screen if login is successful
        else:
            error_message.config(text="Invalid Username or Password")

    # Login button
    login_button = tk.Button(login_frame, text="Login", font=custom_font, command=verify_login, bg="#4CAF50", fg="white", width=10)
    login_button.grid(row=4, column=1, columnspan=2, pady=(10, 20))


# Function to show data permission screen
def show_permission_screen():
    global permission_frame
    permission_frame = tk.Frame(root)
    permission_frame.pack(pady=20)

    # Label for data permission question
    tk.Label(permission_frame, text="Do you consent to allow this app to securely store your data for future use and personalized support?", font=custom_font).pack()
    
    # Button for "Yes" to continue
    tk.Button(permission_frame, text="Yes", font=custom_font, command=lambda: [permission_frame.pack_forget(), show_main_screen()]).pack(pady=5)
    
    # Button for "No" to display a message in red and go back to login
    def deny_permission():
        tk.Label(permission_frame, text="App cannot store user's data, going back to login screen", font=custom_font, fg="red").pack(pady=5)
        root.after(2000, lambda: [permission_frame.pack_forget(), show_login_screen()])  # Delay before returning to login
    
    tk.Button(permission_frame, text="No", font=custom_font, command=deny_permission).pack(pady=5)


# Function to show main mood tracking options
def show_main_screen():
    global main_frame
    main_frame = tk.Frame(root)
    main_frame.pack(pady=20)

    tk.Label(main_frame, text="What would you like to explore today?", font=custom_font).pack(pady=20)

    # Buttons for mood tracking and mood history
    tk.Button(main_frame, text="Track Mood", font=custom_font, command=track_today_mood).pack(pady=5)
    tk.Button(main_frame, text="Mood History", font=custom_font, command=show_mood_graph).pack(pady=5)

def track_today_mood():
    main_frame.pack_forget()
    mood_frame = tk.Frame(root)
    mood_frame.pack(pady=20)

    tk.Label(mood_frame, text="How are you feeling today?", font=custom_font).pack(pady=10)

    # Display current date and time
    current_time = datetime.now().strftime('%B %d, %Y %I:%M %p (EST)')
    tk.Label(mood_frame, text=current_time, font=custom_font).pack(pady=5)

    # Add emoji faces above the slider
    emoji_frame = tk.Frame(mood_frame)
    emoji_frame.pack(pady=10)

    # URLs for emoji images
    emoji_urls = [
        "https://www.pinclipart.com/picdir/big/34-348074_png-download-collection-of-crying-face-high-quality.png",
        "https://www.pngarts.com/files/1/Sad-Face-PNG-Image-with-Transparent-Background.png",
        "https://static.thenounproject.com/png/967517-200.png",
        "https://creazilla-store.fra1.digitaloceanspaces.com/icons/3254689/face-happy-icon-md.png",
        "https://creazilla-store.fra1.digitaloceanspaces.com/emojis/45668/slightly-smiling-face-emoji-clipart-md.png",
        "https://creazilla-store.fra1.digitaloceanspaces.com/icons/3254688/face-delighted-icon-md.png"
    ]

    for url in emoji_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((40, 40), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(emoji_frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack(side=tk.LEFT)

    # Slider for mood selection
    mood_slider = tk.Scale(mood_frame, from_=1, to=6, orient=tk.HORIZONTAL, tickinterval=1, length=300)
    mood_slider.set(3)  # Set default to 'Okay'
    mood_slider.pack(pady=10)

    # Optional notes entry
    tk.Label(mood_frame, text="Optional Notes:", font=custom_font).pack(pady=5)
    note_entry = tk.Entry(mood_frame, width=30, font=("Helvetica", 12))
    note_entry.pack(pady=5)

    tk.Button(mood_frame, text="Save Mood", font=custom_font, command=lambda: save_mood(mood_slider, mood_frame, note_entry)).pack(pady=10)

# Function to save mood and go back to main menu
def save_mood(mood_slider, mood_frame, note_entry):
    mood_level = mood_slider.get()
    mood = {1: "Very Sad", 2: "Sad", 3: "Okay", 4: "Slightly Happy", 5: "Happy", 6: "Very Happy"}[mood_level]
    note = note_entry.get().strip() if note_entry.get().strip() else "N/A"  # Get note or set as N/A

      # Format the date and time
    current_time = datetime.now().strftime('%B %d, %Y %I:%M %p (EST)')

    with open("mood_log.txt", "a") as file:
        file.write(f"{current_time} - Mood: {mood}, Note: {note}\n")

    tk.Label(mood_frame, text="Mood noted! Thank you.", font=custom_font, fg="green").pack()
    root.after(2000, lambda: [mood_frame.pack_forget(), show_main_screen()])

# Function to display mood graph
def show_mood_graph():
    moods = []
    dates = []

    try:
        with open("mood_log.txt", "r") as file:
            for line in file:
                date, mood_info = line.split(" - ")
                mood = mood_info.split(": ")[1].strip().split(",")[0]  # Get the mood only
                moods.append(mood)
                dates.append(date)

        # Map mood to numeric values for plotting
        mood_values = [MOOD_SCALE[mood] for mood in moods]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, mood_values, marker='o', color = "black")
        plt.xticks(rotation=45)
        plt.yticks(list(MOOD_SCALE.values()), list(MOOD_SCALE.keys()))
        plt.title("Mood History Over Time")
        plt.xlabel("Date")
        plt.ylabel("Mood")
        plt.grid()
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        tk.messagebox.showwarning("Warning", "Mood history not found.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")

# Show the initial login screen
show_login_screen()
root.mainloop()


