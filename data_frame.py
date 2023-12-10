import tkinter as tk

from chart import show_chart
from constants import LABELS_TEXT, LABELS_VALUES, STATUS_LABELS_TEXT, UNITS


def create_alarm_status(parent):
    alarm_status = tk.Label(parent, text="Alarm Status", relief=tk.RAISED, width=20, height=2, bg="grey")
    return alarm_status


def update_alarm_status(mass_labels, additional_labels, alarm_status):
    # Check if any label in mass_labels or additional_labels is red
    for label in list(mass_labels.values()) + additional_labels:
        if label.cget("fg") == "red":
            alarm_status.config(bg="red")
            return
    alarm_status.config(bg="grey")


def update_label_from_entry(label, entry, unit):
    # Update the label text with the entry content and append the unit
    label.config(text=entry.get() + unit)


def update_mass_labels(mass_entries, mass_labels):
    try:
        total_mass = sum(float(mass_entries[label].get()) for label in mass_entries if mass_entries[label].get())
    except ValueError:
        # If one or more fields are not valid numbers, do nothing
        return

    # Determine the color based on the sum
    if total_mass < 140:
        color = "blue"
    elif 140 <= total_mass <= 160:
        color = "green"
    else:
        color = "red"

    # Update the label colors
    for label in mass_labels.values():
        label.config(fg=color)


def create_data_frame(parent, time_history, temperature_history, pressure_history):
    middle_frame = tk.Frame(parent, width=400, height=400)

    data_labels = {}
    mass_entries = {}

    for i, label_text in enumerate(LABELS_TEXT):
        label = tk.Label(middle_frame, text=f"{label_text}:")
        value = tk.Label(middle_frame, text=LABELS_VALUES[i])
        label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
        value.grid(row=i, column=1, padx=5, pady=2, sticky="w")
        data_labels[label_text] = value

    for i, status_label in enumerate(STATUS_LABELS_TEXT):
        entry_label = tk.Label(middle_frame, text=f"{status_label}:")
        entry = tk.Entry(middle_frame)
        entry_label.grid(row=i, column=2, padx=5, pady=2, sticky="w")
        entry.grid(row=i, column=3, padx=5, pady=2, sticky="w")
        if status_label in ["Маса чавуну", "Маса лому", "Маса вапна"]:
            mass_entries[status_label] = entry
        entry.bind('<Return>', lambda event, label=data_labels[status_label], e=entry, unit=UNITS[status_label]: update_label_from_entry(label, e, unit))

    temperature_label = data_labels["Температура"]
    pressure_label = data_labels["Тиск кисню"]

    temperature_label.bind("<Button-1>", lambda event: show_chart(parent, {'time': time_history, 'values': temperature_history}, "Temperature"))
    pressure_label.bind("<Button-1>", lambda event: show_chart(parent, {'time': time_history, 'values': pressure_history}, "Pressure"))

    oxygen_label = data_labels["Витрати кисню"]
    mass_labels = {label: data_labels[label] for label in ["Маса чавуну", "Маса лому", "Маса вапна"]}

    return middle_frame, temperature_label, pressure_label, oxygen_label, mass_labels, mass_entries

