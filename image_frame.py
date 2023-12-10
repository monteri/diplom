import tkinter as tk
from PIL import Image, ImageTk
from constants import IMAGE_PATH

def create_image_frame(parent):
    left_frame = tk.Frame(parent, width=200, height=300)
    original_image = Image.open(IMAGE_PATH)
    resized_image = original_image.resize((200, 300))
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(left_frame, image=photo)
    image_label.image = photo  # keep a reference!
    image_label.pack(fill=tk.BOTH, expand=True)
    return left_frame