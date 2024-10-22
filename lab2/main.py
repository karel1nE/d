import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            global img
            img = Image.open(file_path)
            display_image(img)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open image: {e}")

def display_image(image):
    image = image.copy()
    image.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor='nw', image=img_tk)
    canvas.image = img_tk

def sharpen_image():
    if img is None:
        messagebox.showerror("Error", "No image loaded")
        return

    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(img_cv, -1, kernel)
    result = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
    display_image(result)

def morphological_processing():
    if img is None:
        messagebox.showerror("Error", "No image loaded")
        return

    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(img_cv, cv2.MORPH_OPEN, kernel)
    result = Image.fromarray(cv2.cvtColor(morph, cv2.COLOR_BGR2RGB))
    display_image(result)

app = tk.Tk()
app.title("Image Processing App")

canvas = tk.Canvas(app, width=400, height=400)
canvas.pack()

btn_load = tk.Button(app, text="Load Image", command=load_image)
btn_load.pack(side=tk.LEFT)

btn_sharpen = tk.Button(app, text="Sharpen", command=sharpen_image)
btn_sharpen.pack(side=tk.LEFT)

btn_morph = tk.Button(app, text="Morphological", command=morphological_processing)
btn_morph.pack(side=tk.LEFT)

img = None

app.mainloop()