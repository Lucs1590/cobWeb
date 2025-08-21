import os
import tkinter as tk
from PIL import Image, ImageTk


def run_script(script):
    os.system(f'python {script}')


def create_image_button(frame, img_path, text, script):
    img = Image.open(img_path).resize((120, 120), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    images.append(photo)

    lbl = tk.Label(frame, image=photo, bg="white")
    lbl.pack(pady=(10, 5))

    btn = tk.Button(
        frame,
        text=text,
        font=("Century", 12),
        bg="black",
        fg="white",
        command=lambda: run_script(script),
        width=18
    )
    btn.pack(pady=(0, 10))


root = tk.Tk()
root.title("CobWeb.exe")
root.geometry("700x500")
root.configure(background="white")

images = []

title = tk.Label(root, text="CobWeb", font=("Arial", 20, "bold"), bg="white")
title.pack(pady=15)

content = tk.Frame(root, bg="white")
content.pack(expand=True, pady=10)

clima_frame = tk.Frame(content, bg="white")
clima_frame.grid(row=0, column=0, padx=20)

pragas_frame = tk.Frame(content, bg="white")
pragas_frame.grid(row=0, column=1, padx=20)

plantas_frame = tk.Frame(content, bg="white")
plantas_frame.grid(row=0, column=2, padx=20)

create_image_button(
    clima_frame,
    "img/weather.png",
    "Clima",
    "Climas.py"
)
create_image_button(
    pragas_frame,
    "img/bug.png",
    "Pragas",
    "Pragas.py"
)
create_image_button(
    plantas_frame,
    "img/plant.png",
    "Plantas Daninhas",
    "PlantDan.py"
)

# ---------- Exit Button ----------
exit_btn = tk.Button(
    root,
    text="Sair",
    font=("Century", 12),
    bg="black",
    fg="white",
    width=15,
    command=root.quit
)
exit_btn.pack(pady=15)

root.mainloop()
