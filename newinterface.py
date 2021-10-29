import os
import tkinter
import Image
import ttk
from tkinter import Canvas
import ImageTk
top = tkinter.Tk()

top.title('CobWeb.exe')
# Arquitetura
top.geometry("600x400")
top.configure(background="white")


# Funcao
canvas = Canvas(top, bg="black", width=200, height=200)
canvas2 = Canvas(top, bg="black", width=200, height=200)
canvas3 = Canvas(top, bg="black", width=200, height=200)


def Clima():
    os.system('python Climas.py')


def Pragas():
    os.system('python Pragas.py')


def Plantas():
    os.system('python PlantDan.py')


def quit():
    global top
    top.quit()


# Imagem
img = Image.open("abc1.png")
img2 = Image.open("abc2.png")
img3 = Image.open("daninha.png")
img = img.resize((300, 300), Image.ANTIALIAS)
img2 = img2.resize((300, 300), Image.ANTIALIAS)
img3 = img3.resize((300, 300), Image.ANTIALIAS)
photoimage = ImageTk.PhotoImage(img)
photoimage2 = ImageTk.PhotoImage(img2)
photoimage3 = ImageTk.PhotoImage(img3)
canvas2.create_image(150, 150, image=photoimage2)
canvas.create_image(150, 150, image=photoimage)
canvas3.create_image(150, 150, image=photoimage3)

# Botao
LabelF = ttk.Label(top, text="CobWeb", font=("Arial", 16))
LabelF.configure(background="white")
Exit = tkinter.Button(top, font=("Century", 12), text="Sair", command=quit)
Exit.configure(background="black", foreground="white")
Erosion = tkinter.Button(top, font=("Century", 12),
                         text="Clima", command=Clima)
Erosion.configure(background="black", foreground="white")
erva = tkinter.Button(top, font=("Century", 12),
                      text="Plantas Daninhas", command=Plantas)
erva.configure(background="black", foreground="white")
Nivel = tkinter.Button(top, font=("Century", 12),
                       text="Pragas", command=Pragas)
Nivel.configure(background="black", foreground="white")
LabelF.place(relx=0.5, rely=0, anchor="n")
Nivel.place(relx=0.44, rely=0.15, anchor="w")
Erosion.place(relx=0.23, rely=0.15, anchor="e")
canvas.place(relx=0.34, rely=0.50, anchor="e")
canvas2.place(relx=0.34, rely=0.5, anchor="w")
canvas3.place(relx=0.67, rely=0.5, anchor="w")
erva.place(relx=0.98, rely=0.15, anchor="e")
Exit.place(relx=0.5, rely=1, anchor="s")
top.mainloop()
