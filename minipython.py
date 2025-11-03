"""
Typing Speed Tester (Tkinter)

Single-file Python program that opens a GUI where the user types a shown sample
passage. Measures elapsed time, words-per-minute (WPM) and accuracy.

Run with: python typing_speed_tester.py
Requires: Python 3.x (tkinter included in standard library)
"""

import tkinter as tk
from tkinter import messagebox
import time
import random

SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a skill that improves with practice and patience.",
    "Practice makes perfect, so keep typing and track your progress.",
    "Python is a great language for building small tools and utilities.",
    "A journey of a thousand miles begins with a single step.",
    "Consistency and focus help you improve your typing speed and accuracy.",
]

class TypingTester:
    def __init__(self, root):
        self.root = root
        root.title("Typing Speed Tester")
        root.geometry("760x360")
        root.resizable(False, False)

        self.start_time = None
        self.end_time = None
        self.running = False
        self.sample = ""

        # Top frame: sample text
        sample_frame = tk.Frame(root, padx=10, pady=10)
        sample_frame.pack(fill=tk.BOTH)

        tk.Label(sample_frame, text="Type this text:", font=(None, 12, 'bold')).pack(anchor='w')
        self.sample_text = tk.Text(sample_frame, height=4, wrap='word', font=("Consolas", 12))
        self.sample_text.pack(fill=tk.X, pady=(3,6))
        self.sample_text.configure(state='disabled')

        # Middle frame: entry and buttons
        mid = tk.Frame(root, padx=10)
        mid.pack(fill=tk.X)

        tk.Label(mid, text="Your input:", font=(None, 11)).pack(anchor='w')
        self.input_entry = tk.Text(mid, height=4, wrap='word', font=("Consolas", 12))
        self.input_entry.pack(fill=tk.X, pady=(3,6))
        self.input_entry.bind('<Key>', self.on_key_press)

        btn_frame = tk.Frame(root, pady=6)
        btn_frame.pack()

        self.start_btn = tk.Button(btn_frame, text="New Text", width=12, command=self.new_text)
        self.start_btn.grid(row=0, column=0, padx=6)

        self.finish_btn = tk.Button(btn_frame, text="Finish", width=12, command=self.finish)
        self.finish_btn.grid(row=0, column=1, padx=6)

        self.reset_btn = tk.Button(btn_frame, text="Reset", width=12, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=6)

        # Bottom frame: stats
        stats = tk.Frame(root, padx=10, pady=6)
        stats.pack(fill=tk.X)

        self.time_label = tk.Label(stats, text="Time: 0.00 s", font=(None, 11))
        self.time_label.grid(row=0, column=0, sticky='w')

        self.wpm_label = tk.Label(stats, text="WPM: 0.00", font=(None, 11))
        self.wpm_label.grid(row=0, column=1, sticky='w', padx=20)

        self.acc_label = tk.Label(stats, text="Accuracy: 0.00%", font=(None, 11))
        self.acc_label.grid(row=0, column=2, sticky='w', padx=20)

        # initialize
        self.new_text()

    def new_text(self):
        """Select a new sample text and reset state."""
        self.sample = random.choice(SAMPLE_TEXTS)
        self.sample_text.configure(state='normal')
        self.sample_text.delete('1.0', tk.END)
        self.sample_text.insert(tk.END, self.sample)
        self.sample_text.configure(state='disabled')

        self.reset(clear_text=False)

    def reset(self, clear_text=True):
        """Reset timer and stats. Optionally clear the input field."""
        self.start_time = None
        self.end_time = None
        self.running = False
        if clear_text:
            self.input_entry.delete('1.0', tk.END)
        self.time_label.config(text="Time: 0.00 s")
        self.wpm_label.config(text="WPM: 0.00")
        self.acc_label.config(text="Accuracy: 0.00%")

    def on_key_press(self, event):
        """Start timer on first keypress. Ignore modifier keys."""
        if not self.running:
            if len(event.char) == 0:  # ignore non-printable keys
                return
            self.start_time = time.time()
            self.running = True
            # clear stats so they update fresh
            self.time_label.config(text="Time: 0.00 s")
            self.wpm_label.config(text="WPM: 0.00")
            self.acc_label.config(text="Accuracy: 0.00%")

        # optional: auto-finish if input length >= sample length
        typed = self.get_typed_text()
        if len(typed) >= len(self.sample):
            # small delay to allow last key to be registered
            self.finish()

    def get_typed_text(self):
        return self.input_entry.get('1.0', tk.END).rstrip('\n')

    def finish(self):
        if not self.running and not self.start_time:
            messagebox.showinfo("Info", "Start typing first (press any key in the input box) to begin test.")
            return

        self.end_time = time.time()
        elapsed = self.end_time - self.start_time if self.start_time else 0.0
        typed = self.get_typed_text()

        # compute characters correct
        correct_chars = 0
        for i, ch in enumerate(typed):
            if i < len(self.sample) and ch == self.sample[i]:
                correct_chars += 1

        total_typed = len(typed)

        # WPM: (correct_chars / 5) / minutes
        minutes = elapsed / 60 if elapsed > 0 else 1e-9
        wpm = (correct_chars / 5) / minutes

        accuracy = (correct_chars / total_typed * 100) if total_typed > 0 else 0.0

        self.time_label.config(text=f"Time: {elapsed:.2f} s")
        self.wpm_label.config(text=f"WPM: {wpm:.2f}")
        self.acc_label.config(text=f"Accuracy: {accuracy:.2f}%")

        self.running = False

        # optionally show a results popup
        messagebox.showinfo("Results", f"Time: {elapsed:.2f} s\nWPM: {wpm:.2f}\nAccuracy: {accuracy:.2f}%")


if __name__ == '__main__':
    root = tk.Tk()
    app = TypingTester(root)
    root.mainloop()
