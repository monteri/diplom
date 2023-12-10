import tkinter as tk


def create_control_frame(parent, start_stop_callback, time_label):
    bottom_frame = tk.Frame(parent, width=400, height=50)
    start_stop_button = tk.Button(bottom_frame, text="Старт", command=start_stop_callback)
    start_stop_button.pack(side=tk.LEFT, padx=5, pady=5)
    time_label.pack(side=tk.LEFT, padx=5, pady=5)
    return bottom_frame