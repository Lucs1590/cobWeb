import sys
import subprocess

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk


class CobwebApp(tk.Tk):
    """
    An object-oriented Tkinter application for launching agricultural analysis scripts.
    """

    def __init__(self):
        super().__init__()

        self.title("CobWeb")
        self.geometry("750x450")
        self.configure(background="#f0f0f0")

        self.minsize(600, 400)

        self.BG_COLOR = "#f0f0f0"
        self.BUTTON_BG = "#2c3e50"
        self.BUTTON_FG = "#ecf0f1"
        self.TITLE_FONT = tkfont.Font(family="Arial", size=24, weight="bold")
        self.BUTTON_FONT = tkfont.Font(family="Century Gothic", size=12)

        self.image_references = []

        self._create_widgets()
        self._center_window()

    def _center_window(self):
        """Centers the main window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self):
        """Creates and lays out all the widgets in the application."""

        title_label = tk.Label(
            self,
            text="CobWeb",
            font=self.TITLE_FONT,
            bg=self.BG_COLOR
        )
        title_label.pack(pady=(20, 15))

        content_frame = tk.Frame(self, bg=self.BG_COLOR)
        content_frame.pack(expand=True, fill="both", padx=20, pady=10)

        buttons_data = [
            {"img": "img/weather.png", "text": "Clima", "script": "Climas.py"},
            {"img": "img/bug.png", "text": "Pragas", "script": "Pragas.py"},
            {"img": "img/plant.png", "text": "Plantas Daninhas", "script": "PlantDan.py"}
        ]

        for i in range(len(buttons_data)):
            content_frame.grid_columnconfigure(i, weight=1)

        for index, data in enumerate(buttons_data):
            self._create_image_button(
                parent=content_frame,
                img_path=data["img"],
                text=data["text"],
                script=data["script"]
            ).grid(row=0, column=index, padx=15, pady=10, sticky="n")

        exit_button = tk.Button(
            self,
            text="Sair",
            font=self.BUTTON_FONT,
            bg=self.BUTTON_BG,
            fg=self.BUTTON_FG,
            width=15,
            command=self.destroy
        )
        exit_button.pack(pady=20)

    def _create_image_button(self, parent, img_path, text, script):
        """Creates a frame containing an image label and a corresponding button."""
        frame = tk.Frame(parent, bg=self.BG_COLOR)

        try:

            img = Image.open(img_path).resize(
                (120, 120),
                Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(img)
            self.image_references.append(photo)

            img_label = tk.Label(frame, image=photo, bg=self.BG_COLOR)
            img_label.pack(pady=(10, 5))

        except FileNotFoundError:

            placeholder = tk.Label(
                frame, text=f"Imagem\n '{img_path}'\n não encontrada",
                font=(self.BUTTON_FONT.cget("family"), 9),
                bg="#cccccc", fg="black", width=16, height=7
            )
            placeholder.pack(pady=(10, 5))
            print(f"Warning: Image file not found at '{img_path}'")

        button = tk.Button(
            frame,
            text=text,
            font=self.BUTTON_FONT,
            bg=self.BUTTON_BG,
            fg=self.BUTTON_FG,
            command=lambda s=script: self._run_script(
                s
            ),
            width=18
        )
        button.pack(pady=(0, 10))

        return frame

    def _run_script(self, script_name):
        """Runs an external Python script using the subprocess module."""
        print(f"Attempting to run script: {script_name}...")
        try:
            with subprocess.Popen([sys.executable, script_name]):
                pass
        except FileNotFoundError:
            print(f"Error: The script '{script_name}' was not found.")
        except Exception as e:
            print(f"An error occurred while trying to run {script_name}: {e}")


if __name__ == "__main__":
    app = CobwebApp()
    app.mainloop()
