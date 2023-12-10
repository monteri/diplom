import random
import tkinter as tk
from threading import Thread
import time

from image_frame import create_image_frame
from data_frame import create_data_frame, update_mass_labels, create_alarm_status, update_alarm_status
from constants import *

# Timer and start/stop functionality
running = False
start_time = None
timer_thread = None
target_temperature = None
target_pressure = None
temperature_history = []
pressure_history = []
time_history = []

BASE_TEMPERATURE = 20
TEMPERATURE_GROWTH_RATE = 103.3232
TEMPERATURE_TIME_CONSTANT = 0.001
BASE_PRESSURE = 0.1
PRESSURE_GROWTH_RATE = 0.07123
PRESSURE_TIME_CONSTANT = 0.001


def update_timer():
    global running, start_time, target_temperature, target_pressure, temperature_history, pressure_history, time_history
    while running:
        elapsed_time = time.time() - start_time
        time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        time_label.config(text=time_str)

        # Update temperature
        current_temp = float(temperature_label.cget("text").rstrip("°C") or BASE_TEMPERATURE)
        if current_temp < target_temperature:
            current_temp = min(current_temp + TEMPERATURE_GROWTH_RATE - (elapsed_time * 3 if elapsed_time * 3 < TEMPERATURE_GROWTH_RATE else 0), target_temperature)

        if 0 <= current_temp <= 1594:
            color = "blue"
        elif 1595 <= current_temp <= 1665:
            color = "green"
        else:
            color = "red"
        temperature_label.config(text=f"{current_temp:.2f}°C", fg=color)

        # Update pressure
        current_pressure = float(pressure_label.cget("text").rstrip(" МПа") or BASE_PRESSURE)
        if current_pressure < target_pressure:
            current_pressure = min(current_pressure + PRESSURE_GROWTH_RATE, target_pressure)
        if 0.0 <= current_pressure <= 1.19:
            color = "blue"
        elif 1.20 <= current_pressure <= 1.60:
            color = "green"
        else:
            color = "red"
        pressure_label.config(text=f"{current_pressure:.2f} МПа", fg=color)

        time_history.append(time.time() - start_time)
        temperature_history.append(current_temp)
        pressure_history.append(current_pressure)
        update_alarm_status(mass_labels, [temperature_label, pressure_label], alarm_status)

        root.update()
        time.sleep(1)


def get_oxygen_consumption_color(value):
    if value < 5880:
        return "blue"
    elif 5881 <= value <= 6720:
        return "green"
    else:
        return "red"


def start_stop_timer():
    global running, start_time, timer_thread, target_temperature, target_pressure
    if not running:
        running = True
        start_time = time.time()
        target_temperature = random.uniform(1400, 1800)
        target_pressure = random.uniform(1.0, 2.0)
        timer_thread = Thread(target=update_timer)
        timer_thread.start()

        update_mass_labels(mass_entries, mass_labels)

        try:
            oxygen_consumption_entry = oxygen_label.cget("text").split()[0]
            oxygen_consumption_value = float(oxygen_consumption_entry)
            oxygen_color = get_oxygen_consumption_color(oxygen_consumption_value)
            oxygen_label.config(fg=oxygen_color)
        except ValueError:
            # Handle invalid value or empty field
            pass

        start_stop_button.config(text="Стоп")
    else:
        running = False
        start_stop_button.config(text="Старт")
        if timer_thread.is_alive():
            timer_thread.join()

        # Clear the temperature label when stopping
        # temperature_label.config(text="", fg="black")
        # pressure_label.config(text="", fg="black")
        # for label in mass_labels.values():
        #     label.config(fg="black")


# Main window setup
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Process Control Interface")
    root.geometry("800x400")

    # Create frames
    left_frame = create_image_frame(root)
    middle_frame, temperature_label, pressure_label, oxygen_label, mass_labels, mass_entries = create_data_frame(root, time_history, temperature_history, pressure_history)

    # Pack frames
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create the time label and start/stop button in the middle_frame
    time_label = tk.Label(middle_frame, text="00:00:00")
    time_label.grid(row=len(STATUS_LABELS_TEXT), column=3, padx=5, pady=5)

    start_stop_button = tk.Button(middle_frame, text="Старт", command=start_stop_timer)
    start_stop_button.grid(row=len(STATUS_LABELS_TEXT), column=2, padx=5, pady=5, sticky="e")

    alarm_status = create_alarm_status(root)
    alarm_status.pack(side=tk.BOTTOM, pady=10)

    # Start the GUI loop
    root.mainloop()

    # Make sure to stop the timer thread when closing the window
    if running:
        running = False
        if timer_thread.is_alive():
            timer_thread.join()
