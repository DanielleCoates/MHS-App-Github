# TC04 Script
# 10-31-2024

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timezone, timedelta
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    title_label = tk.Label(login_frame, text="MHS: Mental Health Support App", font=("Helvetica", 16, "bold"),
                           bg="#F5F5F5", fg="#333333")
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
    login_button = tk.Button(login_frame, text="Login", font=custom_font, command=verify_login, bg="#4CAF50",
                             fg="white", width=10)
    login_button.grid(row=4, column=1, columnspan=2, pady=(10, 20))


# Function to show data permission screen
def show_permission_screen():
    global permission_frame
    permission_frame = tk.Frame(root)
    permission_frame.pack(pady=20)

    # Label for data permission question
    tk.Label(permission_frame,
             text="Do you consent to allow this app to securely store your data for future use and personalized support?",
             font=custom_font).pack()

    # Button for "Yes" to continue
    tk.Button(permission_frame, text="Yes", font=custom_font,
              command=lambda: [permission_frame.pack_forget(), show_main_screen()]).pack(pady=5)

    # Button for "No" to display a message in red and go back to login
    def deny_permission():
        tk.Label(permission_frame, text="App cannot store user's data, going back to login screen", font=custom_font,
                 fg="red").pack(pady=5)
        root.after(2000,
                   lambda: [permission_frame.pack_forget(), show_login_screen()])  # Delay before returning to login

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


def save_mood(mood_slider, mood_frame, note_entry):
    mood_value = mood_slider.get()
    mood_text = {1: "Very Sad", 2: "Sad", 3: "Okay", 4: "Slightly Happy", 5: "Happy", 6: "Very Happy"}[mood_value]
    note = note_entry.get().strip()

    # Get the current date and time
    today_date = datetime.now().strftime('%B %d, %Y') # only pays attention to the date, not time, and uses local time

    daily_entry_count = 0
    try:
        with open("mood_log.txt", "r") as file:
            for line in file:
                if line.startswith(today_date):
                    daily_entry_count += 1
    except FileNotFoundError:
        daily_entry_count = 0

    if daily_entry_count >= 10:
        messagebox.showwarning("Error", "Daily mood entry limit reached. Please try again tomorrow. \nReview previous entries in 'Mood History'")
    else:
        current_time = datetime.now().strftime("%B %d, %Y %I:%M %p (EST)")
        with open("mood_log.txt", "a") as file:
            file.write(f"{current_time} - Mood: {mood_text}, Note: {note}\n")
        daily_entry_count += 1  # Update the count to include this new entry
        messagebox.showinfo("Success", f"Mood saved successfully! Total entries for today: {daily_entry_count}")
    note_entry.delete(0, tk.END)


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

    # Save Mood button
    tk.Button(mood_frame, text="Save Mood", font=custom_font,
              command=lambda: save_mood(mood_slider, mood_frame, note_entry)).pack(pady=10)

    # Back button to return to main screen
    tk.Button(mood_frame, text="Back", font=custom_font,
              command=lambda: [mood_frame.pack_forget(), show_main_screen()]).pack(pady=5)


# Function to save mood and go back to main menu
def show_mood_graph():
    global main_frame
    main_frame.pack_forget()  # Hide the main frame
    mood_view_frame = tk.Frame(root)
    mood_view_frame.pack(pady=20)

    tk.Label(mood_view_frame, text="Select a date to modify mood entry:", font=custom_font).pack(pady=10)

    moods = []
    dates = []

    # Load existing moods from the file
    try:
        with open("mood_log.txt", "r") as file:
            for line in file:
                date, mood_info = line.split(" - ")
                mood = mood_info.split(": ")[1].strip().split(",")[0]  # Extract mood only
                moods.append(mood)
                dates.append(date)

        # Create a listbox for date selection
        date_listbox = tk.Listbox(mood_view_frame, width=50, height=10)
        for date in dates:
            date_listbox.insert(tk.END, date)
        date_listbox.pack(pady=10)

        # Mood slider and note entry (initially disabled)
        mood_var = tk.IntVar()
        mood_slider = tk.Scale(mood_view_frame, from_=1, to=6, orient=tk.HORIZONTAL, tickinterval=1, length=300,
                               variable=mood_var)
        mood_slider.pack(pady=10)
        mood_slider.config(state="disabled")  # Disable until date is selected

        # Entry for notes
        tk.Label(mood_view_frame, text="Update Notes:", font=custom_font).pack(pady=5)
        note_entry = tk.Entry(mood_view_frame, width=30, font=("Helvetica", 12))
        note_entry.pack(pady=5)
        note_entry.config(state="disabled")  # Disable until date is selected

        # Function to load mood and note data for selected date
        def load_entry():
            selected_index = date_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "Please select a date.")
                return

            # Enable the mood slider and note entry fields
            mood_slider.config(state="normal")
            note_entry.config(state="normal")

            selected_date = dates[selected_index[0]]
            with open("mood_log.txt", "r") as file:
                for line in file:
                    if selected_date in line:
                        mood_info = line.split(" - ")[1]
                        mood = mood_info.split(": ")[1].strip().split(",")[0]
                        note = mood_info.split("Note: ")[1].strip()
                        break

            # Display the mood and note in entry fields for editing
            mood_var.set(MOOD_SCALE[mood])
            note_entry.delete(0, tk.END)
            note_entry.insert(0, note)

        tk.Button(mood_view_frame, text="Load Entry", font=custom_font, command=load_entry).pack(pady=5)

        # Confirm Update button
        def confirm_update():
            selected_index = date_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "Please select a date.")
                return

            selected_date = dates[selected_index[0]]
            new_mood = {1: "Very Sad", 2: "Sad", 3: "Okay", 4: "Slightly Happy", 5: "Happy", 6: "Very Happy"}[
                mood_var.get()]
            new_note = note_entry.get()

            # Update the mood log file
            with open("mood_log.txt", "r") as file:
                lines = file.readlines()

            with open("mood_log.txt", "w") as file:
                for line in lines:
                    if selected_date in line:
                        # Rewrite the line with updated mood and note
                        formatted_date = selected_date.split(" - ")[0]  # Get the date part
                        file.write(f"{formatted_date} - Mood: {new_mood}, Note: {new_note}\n")
                    else:
                        file.write(line)

            messagebox.showinfo("Success", "Mood entry updated successfully!")

        tk.Button(mood_view_frame, text="Confirm Update", font=custom_font, command=confirm_update).pack(pady=5)

        # Back button to return to the main menu
        tk.Button(mood_view_frame, text="Back", font=custom_font,
                  command=lambda: [mood_view_frame.pack_forget(), show_main_screen()]).pack(pady=10)

        # Create the mood graph
        create_mood_graph(dates, moods, mood_view_frame)  # Pass the frame to create the graph

    except FileNotFoundError:
        messagebox.showerror("Error", "Mood log file not found.")


def create_mood_graph(dates, moods, parent_frame):
    # Convert mood names to numerical values for graphing
    mood_values = [MOOD_SCALE[mood] for mood in moods]

    # Create a figure and axis for the graph
    fig = Figure(figsize=(10, 5))  # Increased size for better visibility
    ax = fig.add_subplot(111)
    ax.plot(dates, mood_values, marker='o', linestyle='-', color='b')
    ax.set_xticks(dates)  # Set x-ticks to the dates
    ax.set_xticklabels(dates, rotation=45, ha='right')  # Rotate date labels for better readability
    ax.set_title("Mood History")
    ax.set_xlabel("Date")
    ax.set_ylabel("Mood Level")
    ax.set_ylim(1, 6)  # Set y-axis limits based on mood scale
    ax.grid()

    # Adjust layout to prevent clipping of tick-labels
    fig.tight_layout()

    # Create a canvas to hold the figure and add it to the parent frame
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Define moods and notes for testing with the specified date format
test_entries = [
    ("October 25, 2024 10:00 AM (EST)", "Happy", "Felt great!"),
    ("October 26, 2024 11:30 AM (EST)", "Okay", "N/A"),
    ("October 27, 2024 9:00 AM (EST)", "Sad", "Had a rough day."),
    ("October 28, 2024 2:45 PM (EST)", "Very Happy", "Had an awesome day!"),
    ("October 29, 2024 1:15 PM (EST)", "Slightly Happy", "Things are looking up."),

]

# Write test entries to the mood_log.txt
with open("mood_log.txt", "w") as file:
    for date_str, mood, note in test_entries:
        file.write(f"{date_str} - Mood: {mood}, Note: {note}\n")

print("Test entries added to mood_log.txt.")

# Show the initial login screen
show_login_screen()
root.mainloop()