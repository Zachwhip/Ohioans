# Ohioans_UI.py

import tkinter as tk
from PIL import Image, ImageTk
import Ohioans_File
import Ohioans_Score

def run(start_callback, stop_callback):
    # Create the main window
    root = tk.Tk()
    root.title("Ohioans Cornhole Log Reader")

    # Set window size and minimum size
    root.geometry("398x628")
    root.minsize(398, 628)

    # Open the PNG image
    # logo = Image.open("C:/Users/dylan/Documents/Ohioans/UCLogo.png")
    #logo = Image.open("C:/Users/zachw/Documents/SeniorDesign/Ohioans/UCLogo.png")

    # Save the image as .ico
    # logo.save("C:/Users/dylan/Documents/Ohioans/UCLogo.ico")
    #logo.save("C:/Users/zachw/Documents/SeniorDesign/Ohioans/UCLogo.ico")

    # Set the window icon (using .ico format)
    # root.iconbitmap("C:/Users/dylan/Documents/Ohioans/UCLogo.ico")  # Path to the .ico file
    root.iconbitmap("C:/Users/zachw/Documents/GitHub/Ohioans/UCLogo.ico")  # Path to the .ico file

    # Load the UC Logo
    # logo_image = Image.open("C:/Users/dylan/Documents/Ohioans/UCLogo.png")
    logo_image = Image.open("C:/Users/zachw/Documents/GitHub/Ohioans/UCLogo.png")
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Create a Label widget to hold the image and set it as the background
    background_label = tk.Label(root, image=logo_photo)
    background_label.place(relwidth=1, relheight=1)  # Place the background label to cover the entire window

    # Add a custom font (you can customize the font family, size, etc.)
    custom_font = ("Helvetica", 12)

    # Set background color of root (not used for background but for other components)
    root.config(bg="white")  # If you need a fallback color for non-image areas

    # Title label directly on top of the background image
    title_label = tk.Label(root, text="Ohioans Log Monitor", font=("Helvetica", 16), fg="#333", bg="#ffffff")
    title_label.place(relx=0.5, rely=0.1, anchor="center")  # Position at the top center

    # Status label directly on top of the background image
    status_label = tk.Label(root, text="Status: Stopped", font=custom_font, fg="red", bg="#ffffff")
    status_label.place(relx=0.5, rely=0.25, anchor="center")  # Position below the title label

    # Start button with some padding, color, and font
    start_button = tk.Button(
        root, text="Start Monitoring", command=start_callback, font=custom_font,
        fg="white", bg="#4CAF50", relief="raised", bd=5, padx=20, pady=10
    )
    start_button.place(relx=0.5, rely=0.45, anchor="center")  # Position below the status label

    # Stop button with styling
    stop_button = tk.Button(
        root, text="Stop Monitoring", command=stop_callback, font=custom_font,
        fg="white", bg="#f44336", relief="raised", bd=5, padx=20, pady=10
    )
    stop_button.place(relx=0.5, rely=0.6, anchor="center")  # Position below the start button

    # Tracking whether monitoring is active or not
    is_monitoring = False

    # GameScores Instance
    game_scores = Ohioans_Score.GameScores()

    team_red_score = Ohioans_File.team_1_score
    team_blue_score = Ohioans_File.team_2_score

    # Create labels for displaying the total scores for Team Red and Team Blue
    team_red_score_label = tk.Label(root, text=f"Team Red: {team_red_score}", font=("Helvetica", 14), fg="red", bg="#ffffff")
    team_blue_score_label = tk.Label(root, text=f"Team Blue: {team_blue_score}", font=("Helvetica", 14), fg="blue", bg="#ffffff")
    
    # Place the team score labels below the stop button
    team_red_score_label.place(relx=0.3, rely=0.75, anchor="center")  # Team Red on the left
    team_blue_score_label.place(relx=0.7, rely=0.75, anchor="center")  # Team Blue on the right

    def update_team_scores():
        team_red_score = Ohioans_File.team_1_score
        team_blue_score = Ohioans_File.team_2_score

        # Update the score labels for both teams
        team_red_score_label.config(text=f"Team Red: {team_red_score}")
        team_blue_score_label.config(text=f"Team Blue: {team_blue_score}")

    def increase_red_score():
        Ohioans_File.team_1_score += 1
        update_team_scores()

    def decrease_red_score():
        Ohioans_File.team_1_score = max(0, Ohioans_File.team_1_score - 1)
        update_team_scores()

    def increase_blue_score():
        Ohioans_File.team_2_score += 1
        update_team_scores()

    def decrease_blue_score():
        Ohioans_File.team_2_score = max(0, Ohioans_File.team_2_score - 1)
        update_team_scores()

    red_increase_button = tk.Button(root, text="+", font=("Helvetica", 14), fg="white", bg="red", command=increase_red_score)
    red_decrease_button = tk.Button(root, text="-", font=("Helvetica", 14), fg="white", bg="red", command=decrease_red_score)
    blue_increase_button = tk.Button(root, text="+", font=("Helvetica", 14), fg="white", bg="blue", command=increase_blue_score)
    blue_decrease_button = tk.Button(root, text="-", font=("Helvetica", 14), fg="white", bg="blue", command=decrease_blue_score)
    
    red_increase_button.place(relx=0.3, rely=0.82, anchor="center")
    red_decrease_button.place(relx=0.3, rely=0.88, anchor="center")
    blue_increase_button.place(relx=0.7, rely=0.82, anchor="center")
    blue_decrease_button.place(relx=0.7, rely=0.88, anchor="center")

    # Update the status when the program starts/stops
    def update_status(is_monitoring):
        if is_monitoring:
            status_label.config(text="Status: Monitoring Started", fg="green")
        else:
            status_label.config(text="Status: Monitoring Stopped", fg="red")

    # Update the start and stop functions to update status
    def start_program_with_status():
        nonlocal is_monitoring
        if not is_monitoring:  # Only start if not already monitoring
            start_callback()
            update_status(True)
            is_monitoring = True
            start_button.config(state="disabled")  # Disable start button when monitoring starts
            stop_button.config(state="normal")  # Enable stop button when monitoring starts

    def stop_program_with_status():
        nonlocal is_monitoring
        if is_monitoring:  # Only allow stop if monitoring has started
            stop_callback()
            update_status(False)
            is_monitoring = False
            start_button.config(state="normal")  # Enable start button when monitoring stops
            stop_button.config(state="disabled")  # Disable stop button after stopping monitoring

    # Ensure that closing the window stops the monitoring and closes the app
    def on_closing():
        # Stop the monitoring thread gracefully before closing
        stop_callback()  
        root.quit()  # Exit the mainloop, effectively closing the application

    def refresh_scores():
        update_team_scores()
        root.after(1000, refresh_scores)

    # Set the callback for closing the window (clicking the "X" button)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Update callbacks with the status functions
    start_button.config(command=start_program_with_status)
    stop_button.config(command=stop_program_with_status)

    # Initially disable the stop button since monitoring hasn't started
    stop_button.config(state="disabled")
    
    # Initially disable the start button if monitoring is already in progress (to avoid starting multiple times)
    start_button.config(state="normal")

    refresh_scores()

    # Run the main loop
    root.mainloop()