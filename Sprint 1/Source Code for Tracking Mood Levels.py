# Source Code for Tracking Mood Levels
# Date created: 10-30-2024

#Import all necessary libraries:
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.pyplot as plt

# Define the mood scale mapping
MOOD_SCALE = {
    "Very Sad": 1,
    "Sad": 2,
    "Okay": 3,
    "Slightly Happy": 4,
    "Happy": 5,
    "Very Happy": 6
}

# Define custom font style
custom_font = ("Helvetica", 12, "bold")

# Initialize the main application window
root = tk.Tk()
root.title("Mood Tracker")
root.geometry("400x600")
root.configure(bg="#F5F5F5")  # Light background for a clean look

# Function to handle mood entry
def track_today_mood():
    mood_frame = tk.Frame(root)
    mood_frame.pack(pady=20)

    # Get current date and time formatted
    current_time = datetime.now().strftime('%B %d, %Y %I:%M %p (EST)')

    # Display the current date and time
    tk.Label(mood_frame, text=current_time, font=("Helvetica", 14), bg="#F5F5F5").pack(pady=10)

    tk.Label(mood_frame, text="How are you feeling today?", font=custom_font).pack(pady=10)

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

    # Load and display emojis
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

    # Save mood button
    tk.Button(mood_frame, text="Save Mood", font=custom_font, command=lambda: save_mood(mood_slider, mood_frame)).pack(pady=10)

# Function to save mood
def save_mood(mood_slider, mood_frame):
    mood_level = mood_slider.get()
    mood = {1: "Very Sad", 2: "Sad", 3: "Okay", 4: "Slightly Happy", 5: "Happy", 6: "Very Happy"}[mood_level]

    # Save to file with current date and time
    with open("mood_log.txt", "a") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Mood: {mood}\n")

    tk.Label(mood_frame, text="Mood noted! Thank you.", font=custom_font, fg="green").pack()
    root.after(2000, lambda: mood_frame.pack_forget())  # Hide mood frame after 2 seconds

# Function to display mood graph
def show_mood_graph():
    moods = []
    dates = []

    try:
        with open("mood_log.txt", "r") as file:
            for line in file:
                date, mood_info = line.split(" - ")
                mood = mood_info.split(": ")[1].strip()  # Get the mood only
                moods.append(mood)
                dates.append(date)

        # Map mood to numeric values for plotting
        mood_values = [MOOD_SCALE[mood] for mood in moods]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, mood_values, marker='o', color='black')  # Set line color to black
        plt.xticks(rotation=45)
        plt.yticks(list(MOOD_SCALE.values()), list(MOOD_SCALE.keys()))
        plt.title("Mood History Over Time")
        plt.xlabel("Date")
        plt.ylabel("Mood")
        plt.grid()
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showwarning("Warning", "Mood history not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main application flow
track_today_mood()

# Add a button to show the mood graph
tk.Button(root, text="Show Mood Graph", font=custom_font, command=show_mood_graph).pack(pady=20)

# Run the application
root.mainloop()
