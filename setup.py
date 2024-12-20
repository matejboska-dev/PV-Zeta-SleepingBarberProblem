import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import subprocess
import sys
import os

def validate_chairs(value):
    # Allow empty field or digits only
    if value == "" or value.isdigit():
        if value.isdigit():
            # Check if the number is between 1 and 12
            if 1 <= int(value) <= 12:
                return True
        return True
    return False

def launch_main():
    try:
        # Get the number of chairs
        chairs = chairs_spinbox.get()
        
        # Validate input
        if not chairs.isdigit() or not (1 <= int(chairs) <= 12):
            messagebox.showerror("Error", "Please enter a valid number of chairs (1-12)")
            return
            
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(current_dir, 'main.py')
        
        # Create environment variables for the child process
        env = os.environ.copy()
        env['WAITING_ROOM_CHAIRS'] = chairs
        
        # Launch main.py using Python executable with the environment variable
        subprocess.Popen([sys.executable, main_path], env=env)
        
        # Close the setup window after launching
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Error launching main.py: {e}")

# Create the main window
root = tk.Tk()
root.title("Sleeping Barber Problem - Launcher")

# Set window size and position it in the center of the screen
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Configure the window
root.configure(bg='#f0f0f0')

# Create and pack a frame for better organization
frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(expand=True)

# Create title label
title_label = tk.Label(
    frame,
    text="Sleeping Barber Problem",
    font=('Times', 20, 'bold'),
    bg='#f0f0f0'
)
title_label.pack(pady=20)

# Create chairs configuration frame
chairs_frame = tk.Frame(frame, bg='#f0f0f0')
chairs_frame.pack(pady=10)

# Create label for chairs input
chairs_label = tk.Label(
    chairs_frame,
    text="Number of Waiting Room Chairs:",
    font=('Times', 12),
    bg='#f0f0f0'
)
chairs_label.pack(side=tk.LEFT, padx=5)

# Create spinbox for chairs input
validate_cmd = root.register(validate_chairs)
chairs_spinbox = ttk.Spinbox(
    chairs_frame,
    from_=1,
    to=12,  # Changed from 16 to 12
    width=5,
    validate='key',
    validatecommand=(validate_cmd, '%P')
)
chairs_spinbox.set("4")  # Default value
chairs_spinbox.pack(side=tk.LEFT, padx=5)

# Create the play button
play_button = tk.Button(
    frame,
    text="PLAY",
    command=launch_main,
    font=('Times', 16, 'bold'),
    width=10,
    height=1,
    bg='#4CAF50',
    fg='white',
    relief=tk.RAISED,
    cursor='hand2'
)
play_button.pack(pady=20)

# Start the main loop
root.mainloop()