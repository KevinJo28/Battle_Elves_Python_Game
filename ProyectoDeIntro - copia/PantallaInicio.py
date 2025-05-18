from Funciones import nameScreen, HallOfFame
from tkinter import Button
from constantes import *

#E:Un lienzo canvas, ventanaPrincipal y img de fondo
#S:No retorna nada
#R:No tiene restricciones
def inicio(canvas, ventana, imagen):
    #BotonesInicio

    #Bóton para iniciar juego ejecuta la función nameScreen la cual recibe un canvas y la ventana principal
    btnPlay = Button(ventana, text="Play", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: (nameScreen(canvas, ventana)))
    canvas.create_window(500,400, window=btnPlay)
    #Bóton para ir al salón de la fama, ejecuta la función HallOfFame la cuál recibe un lienzo canvas
    btnFame = Button(ventana, text="Hall Of Fame", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: HallOfFame(canvas))
    canvas.create_window(500,500, window=btnFame)
    #Bóton para cerrar la ventana, ejecua un destroy en la ventana, principal
    btnExit= Button(ventana, text="Exit", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: ventana.destroy())
    canvas.create_window(500,600, window=btnExit)
    
    # Imagen de fondo
    canvas.create_image(0, 0, image=imagen, anchor='nw')
    #Titulo del juego
    canvas.create_text(500, 200, text="Battle \n Elves", font=('Times', 80, 'bold'), fill="white")
    
    

