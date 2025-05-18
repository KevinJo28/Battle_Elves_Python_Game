from tkinter import *
import os
import winsound
from PIL import Image, ImageTk
import pygame
import random
from PlayersAndMobs import *
import pickle

#Funcion para cargar imagen
#E:Nombre de la imagen(str), ancho y alto
#S:Imagen redimensionada en un formato compatible con Tkinter
#R:No tiene
def cargarImagen(fichero, nombre, width, height): 
    ruta = os.path.join(fichero, nombre)
    imagenLoad = Image.open(ruta).resize((width, height))  
    imagen = ImageTk.PhotoImage(imagenLoad)
    return imagen

#Funcion para cambiar imagen derecha
#E:Label que contiene la imagen actual
#S:Cambia el label con la nueva imagen
#R:No tiene
def cambiarImagen(imgPersonal):
        imagen = cargarImagen("assets/images","conFamilia.jpg", 300, 300)
        imgPersonal.config(image=imagen)
        imgPersonal.image = imagen

#Funcion para cambiar imagen izquierda
#E:Label que contiene la imagen actual
#S:Cambia el label con la nueva imagen
#R:No tiene
def cambiarImagen2(imgPersonal):
        imagen = cargarImagen("assets/images","Kevin.jpg", 300, 300)
        imgPersonal.config(image=imagen)
        imgPersonal.image = imagen

#Funcion para abrir ventana con elementos sobre mi
def aboutMe():
    #Ventana principal About
    ventanaAbout = Toplevel()
    ventanaAbout.minsize(740,400)
    ventanaAbout.resizable(False,False)
    ventanaAbout.configure(padx=7, pady=7)
    ventanaAbout.title("About Me")

    #Imagen personal
    imagen = cargarImagen("assets/images", "Kevin.jpg", 300, 300)
    imgPersonal = Label(ventanaAbout, image=imagen)
    imgPersonal.configure(relief=RIDGE, border=5)
    imgPersonal.image = imagen
    imgPersonal.place(x=0,y=0)

    #Botones para pasar las imagenes
    botonFlecha = Button(ventanaAbout, text="⪼", font=("Arial", 10), fg="#890000" , command=lambda: (cambiarImagen(imgPersonal)))
    botonFlecha.place(x=280, y=100)
    botonFlecha2 = Button(ventanaAbout, text="⪻", font=("Arial", 10), fg="#890000" , command=lambda: (cambiarImagen2(imgPersonal)))
    botonFlecha2.place(x=3, y=100)

    #Label del nombre
    nombre = Label(ventanaAbout,text="Nombre: Kevin Abarca Cascante", padx=2, pady=2,anchor=W, bg="#cacaca", fg="#000", font=(30), width=40)
    nombre.place(x=340, y=0)

    #Label de edad
    edad = Label(ventanaAbout,text="Edad: 18", padx=2, pady=2,anchor=W, bg="#cacaca", fg="#000", font=(30), width=40)
    edad.place(x=340, y=40)

    #Label hobbies
    hobbies = Label(ventanaAbout,text="Hobbies: Jugar Ajedrez, Jugar VideoJuegos, Leer, Aprender cosas nuevas", padx=2, pady=2,anchor=W, bg="#cacaca", fg="#000", font=(30), width=40, wraplength=340)
    hobbies.place(x=340, y=80)

    #Imagen de pelicula favorita
    imagen2 = cargarImagen("assets/images", "Pelicula.jpg", 100, 110)
    imgPelicula = Label(ventanaAbout, image=imagen2, relief=SOLID, border=3)
    imgPelicula.img = imagen2
    imgPelicula.place(x=340, y=160)

    #Label pelicula favorita
    peliculaFavorita = Label(ventanaAbout,text="Pelicula Favorita \n \n THE CURIOUS CASE OF BENJAMIN BUTTON", padx=2, pady=2, fg="#000", font=("Times", 14), wraplength=300)
    peliculaFavorita.place(x=460, y=160)

    #Imagen cancion
    imagen3 = cargarImagen("assets/images", "cancion.png", 50, 50)
    imgCancion= Label(ventanaAbout, image=imagen3)
    imgCancion.img = imagen3
    imgCancion.place(x=120, y=320)

    #Boton play
    botonPlay = Button(ventanaAbout, text="▶", font=("Arial", 15), fg="#000" , width=2, command=lambda: (playMusisc()), padx=2, pady=2, relief=SOLID)
    botonPlay.place(x=180, y=327)
    #Boton stop
    botonPlay = Button(ventanaAbout, text="||", font=("Arial", 15), fg="#000" , width=2, command=lambda: (stopMusic()), padx=2, pady=2, relief=SOLID)
    botonPlay.place(x=70, y=327)

#Función para iniciar música de about
def playMusisc():
    pygame.mixer.music.load("assets/sounds/Bon-Jovi-It_s-My-Life.wav")
    pygame.mixer.music.play()
#Funcion para detener música de about
def stopMusic():
    pygame.mixer.music.pause()

#Función para abrir ventana de ayuda
def help():
     ventana = Toplevel()
     ventana.minsize(width=400, height=400)
     ventana.title("Help Page")
     ventana.configure(padx=20, pady=20)
     ventana.resizable(False, False)
     label1 = Label(ventana, text="Hola Aventurero!", font=("Arial", 20, "bold"))
     label1.place(x=0, y=0)
     label2 = Label(ventana, text="Bienvenido a tu nueva aventura por Battle Elves, tu misión es defender la fuente de la vida de los elfos malignos, usa tu arma para defenderla y aventurate por los diferentes niveles, para así lograr entrar al salon de la fama y inmortalizar tu nombre.", font=("Arial", 10), wraplength=340, width=50, justify="left", anchor="w")
     label2.place(x=0, y=50)


#Arreglo de imagenes para que el recolector de no las borre
imagenes = []
#E:Recibe lienzo canvas
def HallOfFame(canva):
    #Guarda los datos de los jugadores que estan en el salón de la fama
    jugadores = CargarDatos()
    #Cargar imagenes de copas
    GoldCup = cargarImagen("assets/images", "GoldCup.png", 120, 120) 
    SilverCup = cargarImagen("assets/images", "SilverCup.png", 120, 120)
    CopperCop = cargarImagen("assets/images", "CopperCop.png", 120, 120)
    #Agregar imagenes a la lista
    imagenes.append(GoldCup)
    imagenes.append(SilverCup)
    imagenes.append(CopperCop)
    #Borra el lienzo completo
    canva.delete("all")
    #Crea las imagenes anteriores en el lienzo
    canva.create_image(200, 200, image=GoldCup, anchor='nw')
    canva.create_image(400, 200, image=SilverCup, anchor='nw')
    canva.create_image(600, 200, image=CopperCop, anchor='nw')
    #Coordenadas para ubicar los nombres
    x = 220
    y = 650
    #For por indice que recorre la lista de jugadores en el salón de la fama y los acomoda
    for i in range(0, len(jugadores)):
        if i + 1 >= 4:
            y+=50
            x=220
            #Crea un texto con el nombre de los primeros tres jugadores
            canva.create_text(x, y, text=f"{i + 1}. {jugadores[i][0]}", font=('times', 15, 'bold'), fill="white")
        else:
            y=160
            #Crea un texto con los demás jugadores
            canva.create_text(x, y, text=f"{i + 1}. {jugadores[i][0]}", font=('times', 20, 'bold'), fill="#efb810")
            x+=220
            y=300
    #Background
    canva.config(bg="#240005")
    canva.update()


#E:lienzo canvas y ventana principal
#Se encargar de mostrar un entry para que el jugardor pueda ingresar su nombre
def nameScreen(canva, ventana):
    #Borra el liezo y le estable un cursor y bg
    canva.delete("all")  
    canva.config(bg="black", cursor="@assets/Mira2.cur")
    #Texto de bienvenida
    canva.create_text(500, 300, text="Ingresa tu nombre, viajero", font=('Helvetica', 40, "bold"), fill="white")
    #Entry para ingresar el nombre
    name = Entry(canva, width=30)
    name.configure(border=5, fg="#7B0323", relief='ridge')
    #Agrega el entry como widget a canvas, para mostrarlo
    canva.create_window(500, 400, window=name)
    #Bóton para empezar juego
    btnContinue = Button(canva, text="Continue", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: game(canva, name.get(), ventana))
    #Agrega el bóton como widget a canvas, para mostrarlo
    canva.create_window(500,500, window=btnContinue)



###############################################################Funciones del lienzo principal del juego#############################################################################################################
#E:Recibe el lienzo canvas, nombre del jugador y ventana principal
#S:Ejecuta el juego, crea el entorno de nivel1, el jugador y enemigos
#R:No tiene restricciones
def game(canva, name, ventana):
    #No se ejecuta hasta el usuario ingrese un nombre
    if name == "":
        return nameScreen(canva)
    #Ejecuta música de fondo
    pygame.mixer.music.load("assets/sounds/SoundTrack.wav")
    pygame.mixer.music.play()
    #En caso de cerrar la ventana detiene la música
    ventana.protocol("WM_DELETE_WINDOW", lambda: detener_sonido(ventana))
    #Limpia el lienzo y le da un bg nuevo y cursor
    canva.delete("all")  
    canva.config(bg="black", cursor="@assets/Mira2.cur")

    #Carga de todas las imagenes necesarias
    imgHeart = cargarImagen("assets/images", "Cuore1.png", 30, 30)
    fountainImg = cargarImagen("assets/images/fountainFrames", "frame-01.png", 70, 70)
    scenery = cargarImagen("assets/images", "nivel1.png", 256, 256)
    HWall = cargarImagen("assets/images", "hWall.png", 64, 32)
    vWall = cargarImagen("assets/images", "vWall.png", 10, 64)
    cloud = cargarImagen("assets/images", "cloud.gif", 1000, 200)
    Cliff_Tile = cargarImagen("assets/images", "Cliff_Tile.png", 64, 80)
    rock = cargarImagen("assets/images", "grass.png", 20, 20)
    grass = cargarImagen("assets/images", "rock.png", 20, 20)
    grass2 = cargarImagen("assets/images", "grass2.png", 30, 30)
    #Agregar las imagenes a la lista para no perderlas
    imagenes.append(imgHeart)
    imagenes.append(fountainImg)
    imagenes.append(scenery)
    imagenes.append(HWall)
    imagenes.append(vWall)
    imagenes.append(cloud)
    imagenes.append(Cliff_Tile)
    imagenes.append(rock)
    imagenes.append(grass)
    imagenes.append(grass2)

    #Empieza a genera el escenario, con dos for uno encargado de llenar las columas de 10 hasta 1500 y el segundo encargado de llenar las filas desde 100 hasta 1000
    for columa in range(10, 1500, 50):
        for  fila in range(100, 1000, 50):
            canva.create_image(fila, columa, image=scenery)

    #Empieza a generar las decoraciónes
    for i in range(100, 600, 200):
        canva.create_image(i, i + 50, image=Cliff_Tile, tag="Cliff_Tile")
    for columa in range(600, 800, 50):
        for fila in range(400, 420, 10):
            canva.create_image(fila - 100 ,  columa , image=grass2)
            canva.create_image(fila, columa  - 400, image=grass2)

    #Creación de la fuente
    createFountain(canva, fountainImg, HWall, vWall)
    #Creación de las nubes
    canva.create_image(500, 5, image=cloud, tag="cloud")
    #Empieza a generar el laberinto
    wallGenerate(canva, HWall, vWall)
    
    #Crea el jugador 
    playerImg = cargarImagen("assets/CharacterSprites", "Capa1.png", 20, 30)
    Player = Players(200, 300, 2, 5, 0, playerImg, 1, name)
    Player.draw(canva)
    Player.hpAux(canva, imgHeart, True)
    Player.move("pj", canva)
    #Eventos para el jugador, se encarga de asignar las teclas de movimiento, disparo y click izquierdo
    #Se le asigna el nombre del jugador
    canva.bind_all("<KeyPress>", lambda e: Player.on_key_press(e, canva, name, ventana))
    canva.bind_all("<KeyRelease>", lambda e:Player.on_key_release(e))
    canva.bind_all("<Button-1>", lambda e: Player.onLeftClick(e, canva, "pj"))
    canva.update()
    #Empieza a generar enemigos
    enemyimg =  cargarImagen("assets/EnemySprites", "Enemys1.png", 20, 30)
    canva.after(3000, enemyGenerate, canva, 4, 2, enemyimg, 1, Player, enemyimg)

    #Contador que se engarga de llevar el tiempo
    timeContainer = canva.create_text(500, 30, text="01:00", fill="white", font=("times", 20), tag="timer")
    update_timer(timeContainer, canva, 90, Player, False, ventana)
    canva.create_text(800, 30, text="Points: 0", fill="white", font=("times", 20), tag="points")

#E:Recibe el lienzo canvas, nombre del jugador ventana principal, puntos
#S:Ejecuta el juego, crea el entorno de nivel1, el jugador y enemigos
#R:No tiene restricciones
def nivel2(canva, name, pts, first, ventana):
    #Limpia e inica de nuevo
    canva.delete("all")
    pygame.mixer.music.load("assets/sounds/SoundTrack.wav")
    pygame.mixer.music.play()
    ventana.protocol("WM_DELETE_WINDOW", lambda: detener_sonido(ventana))
    canva.config(bg="black", cursor="@assets/Mira2.cur")
    #Pantalla de cargar de 5s para mostrar el texto Nivel 2
    canva.create_text(450, 130, text="Nivel 2", font=('Helvetica', 40, "bold"), fill="white")
    if first:
        first = False
        canva.after(5000, nivel2 , canva, name, pts, first, ventana)
    else:
        #Cargar imagenes
        imgHeart = cargarImagen("assets/images", "Cuore1.png", 30, 30)
        fountainImg = cargarImagen("assets/images/fountainFrames", "frame-01.gif", 70, 70)
        scenery = cargarImagen("assets/images", "floor_2.png.", 20, 20)
        HWall = cargarImagen("assets/images", "hWall.png", 64, 32)
        vWall = cargarImagen("assets/images", "vWall.png", 10, 64)
        cloud = cargarImagen("assets/images", "cloud.gif", 1000, 200)
        Cliff_Tile = cargarImagen("assets/images", "Cliff_Tile.png", 64, 80)
        #las agrega a la lista
        imagenes.append(imgHeart)
        imagenes.append(fountainImg)
        imagenes.append(scenery)
        imagenes.append(HWall)
        imagenes.append(vWall)
        imagenes.append(cloud)
        imagenes.append(Cliff_Tile)
        #Genera escenario
        for fila in range(100, 1000, 20):
            for columa in range(0, 1500, 20):
                canva.create_image(columa, fila, image=scenery)
        #Creación de la fuente
        createFountain(canva, fountainImg, HWall, vWall)
        canva.create_image(500, 5, image=cloud, tag="cloud")
        wallGenerate(canva, HWall, vWall)
        #Player
        playerImg = cargarImagen("assets/CharacterSprites", "Capa1.png", 20, 30)
        Player = Players(200, 300, 2, 5, pts, playerImg, 1, name)
        Player.draw(canva)
        Player.hpAux(canva, imgHeart, True)
        Player.move("pj", canva)
        print(Player.name)
        #Eventos del teclado y mouse
        canva.bind_all("<KeyPress>", lambda e: Player.on_key_press(e, canva, name, ventana))
        canva.bind_all("<KeyRelease>", lambda e:Player.on_key_release(e))
        canva.bind_all("<Button-1>", lambda e: Player.onLeftClick(e, canva, "pj"))
        canva.update()
        #Empieza a generar enemigos
        enemyimg =  cargarImagen("assets/Enemy2Sprites", "ogre_idle_anim_f0.png", 32, 36)
        enemyimg2 =  cargarImagen("assets/Enemy3Sprites", "TNT_Purple.png", 32, 36)
        canva.after(3000, enemyGenerate, canva, 2, 5,enemyimg, 3, Player, enemyimg2)
        #Tiempo
        timeContainer = canva.create_text(500, 30, text=f"01:00", fill="white", font=("times", 20), tag="timer")
        update_timer(timeContainer, canva, 180, Player, True, ventana)
        canva.create_text(800, 30, text="Points: 0", fill="white", font=("times", 20), tag="points")
    
#E:canvas, imagen de fuente, pared horizontanl y vertical
def createFountain(canva, img, HWall, VWall):
    #Genera un x aleatorio
    x = random.randint(300, 600)
    #Crea las paredes horizontal que cubren la fuente
    canva.create_image(x - 23, 590, image=HWall, tag="HWall")
    canva.create_image(x + 23, 590, image=HWall, tag="HWall")
    #Crea  las paredes verticales que cubren la fuente
    for y in range(620, 720, 50):
         canva.create_image(x - 50, y, image=VWall, tag="VWall")
         canva.create_image(x + 50, y, image=VWall, tag="VWall")
    canva.create_image(x, 620, image=img, tag="fountain")

#E:canvas, pared horizontal y vertical
#S:Genera el laberinto
#R:No tiene restricciones
def wallGenerate(canva, HWall, VWall):
    #Laberinto
    for x in range(200, 400, 50):
        canva.create_image(x, 200, image=HWall, tag="HWall")
        canva.create_image(x + 206, 400, image=HWall, tag="HWall")
        canva.create_image(x + 100, 200, image=HWall, tag="HWall")
        canva.create_image(x - 100, 394, image=HWall, tag="HWall")
        canva.create_image(x + 416, 510, image=HWall, tag="HWall")
        canva.create_image(x + 316, 290, image=HWall, tag="HWall")
            
    for y in range(216, 400, 40):
        canva.create_image(170, y, image=VWall, tag="VWall")
        canva.create_image(170, y + 300, image=VWall, tag="VWall")
        canva.create_image(380, y , image=VWall, tag="VWall")
        canva.create_image(590, y + 100 , image=VWall, tag="VWall")
        canva.create_image(795, y + 200 , image=VWall, tag="VWall")
        canva.create_image(795, y - 90 , image=VWall, tag="VWall")
    #BORDES
    #Paredes Arriba y abajo
    for x in range(20, 1000, 50):
        canva.create_image(x, 90, image=HWall, tag="HWallUP")
    for x in range(20, 1000, 50):
        canva.create_image(x, 680, image=HWall, tag="HWallDOWM")      
    #Paredes izquierda y derecha 
    for y in range(107, 800, 20):
        for x in range(5, 20, 5):
            canva.create_image(x, y, image=VWall, tag="VWallLEFT")
    for y in range(107, 800, 20):
        for x in range(990, 1000, 5):
            canva.create_image(x, y, image=VWall, tag="VWallRIGTH")

    
         
    
    
#Generador de enemigos, cada 3s, no pueden haber mas de 5
#E:canvas, velocidad de movimiento, velocidad de disparo, imagen de enemigo, vida, player y segunda imagen de enemigo
#S:Genera enemigos
#R:No tiene restricciones
def enemyGenerate(canva, speed, speedShot, enemyimg, hp, Player, enemyimg2):
    #Genera enemigos cada 3s
    #Si la fuente y el corazon son visibles, genera enemigos
    if canva.find_withtag("heart5") and canva.find_withtag("timer") and canva.find_withtag("fountain"):
        imgBrokenHeart = cargarImagen("assets/images", "brokenCuore.png", 30, 30)
        #Crea enemigos de diferente imagen y los dibuja en el canvas
        #Usa la funcion de visionZone para que los enemigos puedan atacar al jugador
        #Usa la funcion hpAux para que el jugador pueda atacarlo
        #Si no esta la etiqueta genera el enemigo
        if not canva.find_withtag("Enemy1"):
            Enemy1= Enemies(random.randint(100, 300), random.randint(380, 450), speed, speedShot, enemyimg, hp)
            Enemy1.draw(canva, 1)
            Enemy1.enemyMove(canva, 0, 0, random.randint(0, 3), "Enemy1")
            Enemy1.visionZone(canva, "Enemy1", imgBrokenHeart)
            Enemy1.hpAux(canva, "Enemy1", Player)

        if not canva.find_withtag("Enemy2"):
            Enemy2 = Enemies(random.randint(400, 500), random.randint(400, 510), speed, speedShot, enemyimg, hp)
            Enemy2.draw(canva, 2)
            Enemy2.enemyMove(canva, 0, 0, random.randint(0, 3), "Enemy2")
            Enemy2.visionZone(canva, "Enemy2", imgBrokenHeart)
            Enemy2.hpAux(canva, "Enemy2", Player)

        if not canva.find_withtag("Enemy3"):
            Enemy3 = Enemies(random.randint(20, 100), random.randint(200, 270), speed, speedShot, enemyimg2, hp)
            Enemy3.draw(canva, 3)
            Enemy3.enemyMove(canva, 0, 0, random.randint(0, 3), "Enemy3")
            Enemy3.visionZone(canva, "Enemy3", imgBrokenHeart)
            Enemy3.hpAux(canva, "Enemy3", Player)

        if not canva.find_withtag("Enemy4"):
            Enemy4 = Enemies(random.randint(250, 370), random.randint(400, 470), speed, speedShot, enemyimg2, hp)
            Enemy4.draw(canva, 4)
            Enemy4.enemyMove(canva, 0, 0, random.randint(0, 3), "Enemy4")
            Enemy4.visionZone(canva, "Enemy4", imgBrokenHeart)
            Enemy4.hpAux(canva, "Enemy4", Player)

        if not canva.find_withtag("Enemy5"):
            Enemy5 = Enemies(random.randint(100, 700), random.randint(100, 130), speed, speedShot, enemyimg, hp)
            Enemy5.draw(canva, 5)
            Enemy5.enemyMove(canva, 0, 0, random.randint(0, 3), "Enemy5")
            Enemy5.visionZone(canva, "Enemy5", imgBrokenHeart)
            Enemy5.hpAux(canva, "Enemy5", Player)
        
        canva.after(3000, enemyGenerate, canva, speed, speedShot, enemyimg, hp, Player, enemyimg2)
    else:
         return
   
    

#Funcion para actualizar el tiempo
#E:Recibe el contenedor de tiempo, lienzo canvas, contador, jugador, segundo nivel y ventana principal
#S:Actualiza el tiempo
#R:No tiene restricciones
def update_timer(timeContainer, canva, count, Player, nvl2, ventana):
    #Si el contador es mayor a cero y el jugador tiene vida, el tiempo sigue
    #Si el contador es menor a cero y el jugador no tiene vida, se detiene la musica y muestra la pantalla de game over
    #Si el jugador gana se muestra la pantalla de victoria
    if count < 0 and not canva.find_withtag("heart5") and not canva.find_withtag("fountain"):
        pygame.mixer.music.stop()
        gameOver = pygame.mixer.Sound("assets/sounds/GameOver.mp3")
        gameOver.set_volume(0.5)
        gameOver.play()
        canva.create_text(450, 130, text="Game Over", font=('Helvetica', 40, "bold"), fill="white")
        for i in range(6):
            canva.delete(f"Enemy{i}")
        canva.delete("timer")
        canva.after(4000, lambda: nameScreen(canva, ventana))
        return
    #Si el contador es mayor o igual a cero y el jugador tiene vida, se actualiza el tiempo
    if count >= 0 and canva.find_withtag("timer") and canva.find_withtag("heart5") and canva.find_withtag("fountain"):
        if canva.find_withtag("broken5") and not canva.find_withtag("timer"):
            return
        seconds = count % 60
        minutes = count // 60
        canva.itemconfig(timeContainer, text=f"{minutes:02}:{seconds:02}")
        canva.after(1000, update_timer, timeContainer, canva, count - 1, Player, nvl2, ventana)
    #Si se acaba el tiempo y tiene vida y la fuente esta bien muestra la animación de victoria
    elif canva.find_withtag("heart5") and canva.find_withtag("fountain"):
        canva.create_text(450, 130, text="You win", font=('Helvetica', 40, "bold"), fill="white")
        canva.delete("timer")
        #Borra enemigos
        for i in range(6):
            canva.delete(f"Enemy{i}")
        #Pausa la música
        pygame.mixer.music.pause()
        #Reproduce la de victoria
        victory = pygame.mixer.Sound("assets/sounds/Win.wav")
        victory.set_volume(0.5)
        victory.play()
        #Animación de fuegos artificiales
        win(0, canva,  random.randint(60, 300), random.randint(60, 300), 100)
        #Si no estamos en el nivel dos lo ejecuta luego de 4s
        if not nvl2: canva.after(4000, nivel2, canva, Player.name, Player.points, True, ventana)
        #Si estamos en el nivel y gana, entonces verifica si entra al salón de la fama
        if nvl2:
            #Juarda nombre y puntos en una lista con tuplas
            jugadores = [(Player.name, Player.points)]
            #Carga los datos anteriores si hay
            jugadoresLeidos=CargarDatos()
            #Lista para colocar puntos
            puntos = []
            #Colocar todos los puntos
            for i in jugadoresLeidos:
                puntos.append(i[1])
            #Los acomoda de mayor a menor
            puntos = sorted(puntos, reverse=True)
            #Si hay puntos antertioes verifica
            if puntos != []:
                for i in puntos:
                    #Los puntos son mayores que la posición que se verifica
                    if jugadores[0][1] > i:
                        canva.create_text(450, 200, text=f"Estas en el salón de la fama {Player.name}, con {Player.points} pts", font=('Helvetica', 20, "bold"), fill="#efb810")
                        btn = Button(canva, text="Ir al Salón de la fama", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: HallOfFame(canva))
                        canva.create_window(450,300, window=btn)
                        GuardarDatos(jugadores)
                        break
                    #No hay jugadores o menos de 5
                    elif jugadoresLeidos == [] or len(jugadoresLeidos) < 5:
                        canva.create_text(450, 200, text=f"Estas en el salón de la fama {Player.name}", font=('Helvetica', 20, "bold"), fill="#efb810")
                        btn = Button(canva, text="Ir al Salón de la fama", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: HallOfFame(canva))
                        canva.create_window(450,300, window=btn)
                        GuardarDatos(jugadores)
                        break  
            #No hay puntos     
            elif puntos == []:
                canva.create_text(450, 230, text=f"Estas en el salón de la fama {Player.name}", font=('Helvetica', 20, "bold"), fill="#efb810")
                btn = Button(canva, text="Ir al Salón de la fama", width=20, height=2, font=('Arial', 12, 'bold'), padx=3, pady=3, relief="groove", command=lambda: HallOfFame(canva))
                canva.create_window(500,400, window=btn)
                GuardarDatos(jugadores) 
        print(CargarDatos())
imagenesWin = [] 
def win(cont, canva,x , y, time):
    if time <= 3000:
        if cont > 7:
            canva.delete("fireWorks")
            cont = 0
            x = random.randint(100, 700)
            y = x = random.randint(100, 700)
        img = cargarImagen("assets/images/fireWorksFrames", f"firework_red{cont}.png", 40, 40)
        imagenes.append(img)
        canva.create_image(x + random.randint(100,  300), y - random.randint(100,  300), image=img, tag="fireWorks")
        canva.create_image(x + random.randint(100,  300), y + random.randint(100,  300), image=img, tag="fireWorks")
        canva.create_image(x + random.randint(100,  300), y + random.randint(100,  300), image=img, tag="fireWorks")
        canva.create_image(x + random.randint(100,  300), y + random.randint(100,  300), image=img, tag="fireWorks")
        canva.create_image(x + random.randint(100,  300), y + random.randint(100,  300), image=img, tag="fireWorks")
        canva.create_image(x + random.randint(100,  300), y + random.randint(100,  300), image=img, tag="fireWorks")
        cont+=1
        canva.after(100, win, cont, canva, x, y, time + 100)

#Funcion guardar datos
#E:Recibe una lista de jugadores
#S:Guarda los jugadores en un archivo
#R:No tiene restricciones
def GuardarDatos(jugadores_nuevos):
    try:
        # cargar los jugadores existentes
        with open("jugadores.pkl", "rb") as archivo:
            jugadores_existentes = pickle.load(archivo)
    except (FileNotFoundError, EOFError):
        jugadores_existentes = []
    # Agregar los nuevos jugadores a la lista existente
    jugadores_existentes.extend(jugadores_nuevos)
    # Guardar toda la lista de vuelta al archivo, los acomoda por puntos
    jugadores_existentes = sorted(jugadores_existentes, key= lambda player: player[1], reverse=True)
    if len(jugadores_existentes) > 5:
        jugadores_existentes = jugadores_existentes[:5]
    with open("jugadores.pkl", "wb") as archivo:
        pickle.dump(jugadores_existentes, archivo)
#Funcion cargar datos
def CargarDatos():
    try:
        with open("jugadores.pkl", "rb") as archivo:
            jugadores_cargados = pickle.load(archivo)
        return jugadores_cargados
    except((FileNotFoundError, EOFError)):
        return []
        
def ReproducirSonido(fichero, name):
    ruta = os.path.join(fichero, name)
    winsound.PlaySound(ruta,winsound.SND_FILENAME)


def detener_sonido(ventana):
    ventana.destroy() 
    pygame.mixer.music.pause()


    