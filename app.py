import tkinter as tk
from tkinter import messagebox
import time
import random
import csv
import os
from datetime import datetime
import requests # <--- ADD THIS IMPORT

# --- Constants ---
APP_TITLE = "Typing Speed Test"
WINDOW_GEOMETRY = "800x500"
BG_COLOR = "#f0f0f0"
FONT_NAME = "Helvetica"
FONT_SIZE_NORMAL = 14
FONT_SIZE_LARGE = 18
FONT_SIZE_STATS = 12

CORRECT_COLOR = "#2E8B57"  # SeaGreen
INCORRECT_COLOR = "#DC143C" # Crimson
DEFAULT_TEXT_COLOR = "#333333"

# --- Flask Server URL ---
# This is where your game will send the data.
FLASK_API_URL = "http://127.0.0.1:5000/api/save_result" # <--- ADD THIS

# --- Sample Sentences for the Test ---
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Never underestimate the power of a good book.",
    "The journey of a thousand miles begins with a single step.",
    "Programming is the art of telling another human what one wants the computer to do.",
    "Practice makes perfect when it comes to typing speed and accuracy.",
    "The best time to plant a tree was twenty years ago. The second best time is now.",
    "Life is what happens to you while you are busy making other plans.",
    "Technology is best when it brings people together and makes life easier.",
    "Success is not final, failure is not fatal, it is the courage to continue that counts.",
    "The only way to do great work is to love what you do and stay passionate.",
    "She has a very cheerful and optimistic personality.",
]

# --- CSV File for Progress Tracking ---
PROGRESS_FILE = "typing_progress.csv"

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.config(bg=BG_COLOR, padx=20, pady=20)

        # State variables
        self.sample_text = ""
        self.test_running = False
        self.test_completed = False  # NEW: Track if test is completed
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_job = None  # NEW: Track the timer job for proper cleanup

        # Create and layout widgets
        self.setup_ui()

        # Load the first test
        self.reset_test()
        
        # Check for CSV file and create if it doesn't exist
        self.init_progress_file()

    def setup_ui(self):
        # --- Title ---
        title_label = tk.Label(
            self.root,
            text="Typing Speed Test",
            font=(FONT_NAME, 24, "bold"),
            bg=BG_COLOR,
            fg=DEFAULT_TEXT_COLOR
        )
        title_label.pack(pady=(0, 20))

        # --- Sample Text Display ---
        self.sample_text_widget = tk.Text(
            self.root,
            font=(FONT_NAME, FONT_SIZE_LARGE),
            wrap=tk.WORD,
            height=3,
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        self.sample_text_widget.pack(fill=tk.X)
        self.sample_text_widget.config(state=tk.DISABLED)

        # --- User Input Text Box ---
        self.input_text = tk.Text(
            self.root,
            font=(FONT_NAME, FONT_SIZE_LARGE),
            wrap=tk.WORD,
            height=3,
            padx=10,
            pady=10,
            bd=2,
            relief="groove"
        )
        self.input_text.pack(fill=tk.X, pady=(10, 0))
        self.input_text.focus() 
        self.input_text.bind("<KeyRelease>", self.check_input)

        # --- Stats Frame ---
        stats_frame = tk.Frame(self.root, bg=BG_COLOR)
        stats_frame.pack(fill=tk.X, pady=20)
        
        self.time_label = tk.Label(stats_frame, text="Time: 0s", font=(FONT_NAME, FONT_SIZE_STATS), bg=BG_COLOR)
        self.time_label.pack(side=tk.LEFT, expand=True)

        self.wpm_label = tk.Label(stats_frame, text="WPM: 0", font=(FONT_NAME, FONT_SIZE_STATS), bg=BG_COLOR)
        self.wpm_label.pack(side=tk.LEFT, expand=True)

        self.accuracy_label = tk.Label(stats_frame, text="Accuracy: 100%", font=(FONT_NAME, FONT_SIZE_STATS), bg=BG_COLOR)
        self.accuracy_label.pack(side=tk.LEFT, expand=True)

        # --- Reset Button ---
        self.reset_button = tk.Button(
            self.root,
            text="New Test",
            font=(FONT_NAME, FONT_SIZE_NORMAL),
            command=self.reset_test
        )
        self.reset_button.pack(pady=10)

    def init_progress_file(self):
        """Creates the CSV file with a header if it doesn't exist."""
        if not os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "WPM", "Accuracy"])

    def save_progress(self, wpm, accuracy):
        """Appends the result of a completed test to the CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(PROGRESS_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, wpm, accuracy])
        except IOError as e:
            messagebox.showerror("Save Error", f"Could not save progress to local file: {e}")

    def send_progress_to_server(self, wpm, accuracy):
        """Sends the result to the Flask web server."""
        payload = {
            "wpm": wpm,
            "accuracy": accuracy
        }
        try:
            response = requests.post(FLASK_API_URL, json=payload, timeout=5)
            if response.status_code == 200:
                print("Successfully sent data to the server.")
            else:
                print(f"Failed to send data. Server responded with: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # This will catch connection errors, timeouts, etc.
            print(f"Could not connect to the server: {e}")
            messagebox.showwarning("Server Offline", "Could not send data to the web dashboard. Is the server running?")
    
    def start_test(self):
        """Starts the typing test timer."""
        if not self.test_running and not self.test_completed:
            self.test_running = True
            self.start_time = time.time()
            self.update_timer()

    def stop_timer(self):
        """Stops the timer and cancels any pending timer jobs."""
        self.test_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def update_timer(self):
        """Updates the timer display."""
        if self.test_running and not self.test_completed:
            self.elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"Time: {self.elapsed_time:.1f}s")
            self.timer_job = self.root.after(100, self.update_timer)

    def check_input(self, event):
        """Called on every key release in the input box."""
        # Ignore input if test is already completed
        if self.test_completed:
            return
            
        # Start test on first valid keystroke (ignore special keys)
        if not self.test_running and event.keysym not in ['Return', 'Tab', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            self.start_test()

        typed_text = self.input_text.get("1.0", "end-1c")
        
        # Remove trailing newlines that might be added by Enter key
        typed_text = typed_text.rstrip('\n\r')
        typed_len = len(typed_text)

        # Update the display colors
        self.sample_text_widget.config(state=tk.NORMAL)
        self.sample_text_widget.tag_remove("correct", "1.0", tk.END)
        self.sample_text_widget.tag_remove("incorrect", "1.0", tk.END)

        correct_chars = 0
        for i, char in enumerate(typed_text):
            if i < len(self.sample_text):
                if char == self.sample_text[i]:
                    correct_chars += 1
                    self.sample_text_widget.tag_add("correct", f"1.{i}", f"1.{i+1}")
                else:
                    self.sample_text_widget.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
        
        self.sample_text_widget.config(state=tk.DISABLED)

        # Calculate stats
        wpm = 0
        accuracy = 100
        
        if typed_len > 0:
            accuracy = (correct_chars / typed_len) * 100
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")

        if self.elapsed_time > 0:
            wpm = (correct_chars / 5) / (self.elapsed_time / 60)
            self.wpm_label.config(text=f"WPM: {wpm:.2f}")

        # Check if test is complete
        if typed_len >= len(self.sample_text) and not self.test_completed:
            self.complete_test(wpm, accuracy)

    def complete_test(self, wpm, accuracy):
        """Handles test completion."""
        self.test_completed = True
        self.stop_timer()  # Stop the timer immediately
        self.input_text.config(state=tk.DISABLED)
        
        # Calculate final stats using the elapsed time at completion
        final_wpm = float(f"{wpm:.2f}")
        final_accuracy = float(f"{accuracy:.1f}")
        
        # Save the progress locally
        self.save_progress(final_wpm, final_accuracy)
        
        # Send progress to server
        self.send_progress_to_server(final_wpm, final_accuracy)
        
        messagebox.showinfo(
            "Test Complete!",
            f"Your final score:\n\nWPM: {final_wpm}\nAccuracy: {final_accuracy}%\n\nProgress saved. Check your web dashboard!"
        )

    def reset_test(self):
        """Resets the test to start fresh."""
        # Stop any running timer
        self.stop_timer()
        
        # Reset all state variables
        self.test_running = False
        self.test_completed = False
        self.start_time = 0
        self.elapsed_time = 0
        self.sample_text = random.choice(SAMPLE_TEXTS)
        
        # Reset UI
        self.time_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100%")
        
        # Reset sample text display
        self.sample_text_widget.config(state=tk.NORMAL)
        self.sample_text_widget.delete("1.0", tk.END)
        self.sample_text_widget.insert("1.0", self.sample_text)
        self.sample_text_widget.config(state=tk.DISABLED)
        self.sample_text_widget.tag_config("correct", foreground=CORRECT_COLOR)
        self.sample_text_widget.tag_config("incorrect", foreground=INCORRECT_COLOR, underline=True)
        
        # Reset input text
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.input_text.focus()

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()