"""
Digital Clock GUI application using Tkinter.

This program creates a modern dark-themed clock window that displays the
current local time in HH:MM:SS format and refreshes automatically every second.
"""

import tkinter as tk
from time import strftime


# ----------------------------- Window Setup -----------------------------
# Create the main application window and configure its basic appearance.
root = tk.Tk()
root.title("Digital Clock")
root.geometry("520x240")
root.resizable(False, False)
root.configure(bg="#111827")


# ----------------------------- Header Label -----------------------------
# Add a title label so users know what the application is.
title_label = tk.Label(
    root,
    text="Digital Clock",
    font=("Segoe UI", 24, "bold"),
    bg="#111827",
    fg="#E5E7EB",
)
title_label.pack(pady=(30, 10))


# ----------------------------- Clock Display -----------------------------
# Create the large time label that will be updated every second.
clock_label = tk.Label(
    root,
    font=("Consolas", 58, "bold"),
    bg="#111827",
    fg="#22D3EE",
)
clock_label.pack(pady=10)


# ----------------------------- Time Update Logic -----------------------------
# Get the current time, update the label, and schedule the next refresh.
def update_time():
    """Update the clock label with the current time every second."""
    current_time = strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)


# ----------------------------- Application Start -----------------------------
# Start the clock update loop, then run the Tkinter event loop.
update_time()
root.mainloop()