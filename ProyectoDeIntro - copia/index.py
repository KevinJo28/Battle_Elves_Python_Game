from tkinter import *
from Funciones import *
from constantes import *
from PantallaInicio import inicio
pygame.mixer.init()
#Venta principal del Juego
ventana = Tk()
ventana.minsize(width=WIDTHSCREEN, height=HEIGHTSCREEN)
ventana.title("Battle elves")
ventana.resizable(False, False)
canvas = Canvas(ventana)
canvas.pack(fill='both', expand=True)
#Imagen de fondo de patalla de inicio
imagen = cargarImagen("assets/images", "walpapper.jpg", WIDTHSCREEN,  HEIGHTSCREEN)

#Funcion que se encarga de creear los elementos de inicio
inicio(canvas, ventana, imagen)
#Menu1
navbar = Menu()
navbar.add_command(label="Help", command=lambda: help())
navbar.add_command(label="About", command=lambda: aboutMe())
ventana.config(menu=navbar)
ventana.mainloop()