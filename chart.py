import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_chart(root, data, title):
    # Create a new Tkinter window
    new_window = tk.Toplevel(root)
    new_window.title(title)

    # Create a figure for the plot
    fig, ax = plt.subplots()
    ax.plot(data['time'], data['values'])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(title)
    ax.set_title(f'{title} over Time')

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)