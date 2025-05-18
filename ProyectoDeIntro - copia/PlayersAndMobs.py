# Importaciones necesarias
import math
import random
import threading
import winsound
import pygame
from constantes import *  # Se asume que contiene constantes como tamaños, colores, etc.
import os
from PIL import Image, ImageTk  # Para manejar imágenes en Tkinter

# Función para cargar y redimensionar imágenes
def cargarImagen(fichero, nombre, width, height): 
    ruta = os.path.join(fichero, nombre)
    imagenLoad = Image.open(ruta).resize((width, height))  
    imagen = ImageTk.PhotoImage(imagenLoad)
    return imagen

images = []  # Lista global de imágenes (puede usarse como caché o para referencia)

# Clase que representa al jugador
class Players:
    def __init__(self, x, y, speed, hp, points, playerImg, frame, name):
        # Inicialización de atributos del jugador
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.points = points
        self.playerImg = playerImg
        self.frame = frame
        self.key = set()
        self.name = name

    # Dibuja al jugador en el canvas
    def draw(self, canva):
        canva.create_rectangle(10, 20, 30, 50, fill=None, outline="", tag="pj")
        canva.create_image(self.x, self.y, image=self.playerImg, anchor="nw", tag="pjSprite")
        canva.move("pj", self.x - 10, self.y - 20)
        canva.update()

    # Manejo de vida y animaciones de muerte
    def hpAux(self, canva, imgHeart, reiniciar):
        if not canva.find_withtag("heart5") and not canva.find_withtag("broken5"):
            # Dibuja los corazones si no están dibujados
            x = 10
            y = 10
            for i in range(1, self.hp + 1):
                canva.create_image(x, y, image=imgHeart, anchor="nw", tag=f"heart{i}")
                x += 50
        elif canva.find_withtag("broken5"):
            # Animación de muerte si se ha roto el corazón
            if self.frame > 1 and reiniciar:
                reiniciar = False
                self.frame = 1
            ancho = 18
            alto = 27
            if self.frame > 7:
                return
            elif self.frame == 3:
                ancho = 21
                alto = 19
            elif self.frame > 5:
                ancho = 29
                alto = 11
            self.playerImg = cargarImagen("assets/CharacterSprites", f"Kill{self.frame}.png", ancho, alto)
            self.frame += 1
            canva.itemconfig("pjSprite", image=self.playerImg)
        # Llama a sí misma de forma recursiva
        canva.after(500, self.hpAux, canva, imgHeart, reiniciar)

    # Disparo del jugador al hacer clic izquierdo
    def onLeftClick(self, e, canva, pj):
        #Si no tiene vidad dispara
        if not canva.find_withtag("broken5"):
            disparo_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
            disparo_sound.set_volume(1)
            disparo_sound.play()
            pjcord = canva.coords(pj)
            bala = canva.create_oval(18, 10, 10, 18, fill="red", tag="balaPlayer")
            x = pjcord[0]
            y = pjcord[1]
            canva.move(bala, x, y)
            canva.update()
            self.shoot(e.x, e.y, bala, canva, x, y)

    # Movimiento de la bala disparada por el jugador
    def shoot(self, xFinal, yFinal, bala, canva, xBala, yBala):
        #Si existe la bala entra
        if canva.find_withtag(bala):
            balaCords = canva.coords("balaPlayer")
            #Busca los elementos que esten tocando las corddenadas proporcionadas del elemento principal
            overlapping = canva.find_overlapping(*balaCords)
            #Recorre la lista con los elementos encima
            for item in overlapping:
                if "HWall" in canva.gettags(item) or "VWall" in canva.gettags(item):
                    canva.delete(item)
                    canva.delete(bala)
            #Distancia entrepuntos para saber cuanto falta para llegar al mouse
            distancia = round(math.sqrt((xFinal - xBala)**2 + (yFinal - yBala)**2))
            if distancia < 5:
                canva.delete(bala)
                return
            #Aumenta proporcionamete el x y y para que tenga una dirección real
            velocidadX = ((xFinal - xBala) / distancia) * 5  
            velocidadY = ((yFinal - yBala) / distancia) * 5 
            canva.move(bala, velocidadX, velocidadY)
            canva.update()
            # Mueve la bala cada 20 ms
            canva.after(20, self.shoot, xFinal, yFinal, bala, canva, xBala + velocidadX, yBala + velocidadY)

    # Manejo de teclas presionadas
    def on_key_press(self, e, canva, name, ventana):
        from Funciones import game
        #Si no tiene vida o la fuente esta rota y preciona x reinicia el juego
        if (canva.find_withtag("broken5") or canva.find_withtag("breakFountain")) and e.keysym == "x":
            canva.delete("all")
            self.points = 0
            return game(canva, name, ventana)
        #Agrega las teclas al set
        self.key.add(e.keysym)

    # Manejo de teclas soltadas 
    def on_key_release(self, e):
        #quita las teclas del set
        self.key.discard(e.keysym)

    #Funcion para moverse
    #E:envento, canvas del pj, posicion inicial en x & y, canvas
    def move(self, pj, canva):
        if not canva.find_withtag("broken5") and canva.find_withtag(pj) and not canva.find_withtag("breakFountain"):
            x = 0
            y = 0
            posicion = canva.coords(pj)
            coordFountain = canva.coords("fountain")
            #Veridica que esta tocando las coordenadas proporcionadas del elemento
            overlapping = canva.find_overlapping(posicion[0]-9, posicion[1]-9, posicion[2]+10, posicion[3]+9)
            #Variables para detener movimiento al tocar la pared
            colisiony1 = True
            colisiony2 = True
            colisionx1 = True
            colisionx2 = True

            for item in overlapping:
                coordsItem = canva.coords(item)

                if "HWall" in canva.gettags(item):
                    #Colision Arriba  y Abajo
                    if (posicion[0] + 45 >= coordsItem[0] and posicion[2] <= coordsItem[0] + 45 and posicion[1] <= coordsItem[1]  + 47  and posicion[1] + 35 >= coordsItem[1]):
                        colisiony1 = False
                    if (posicion[0] + 45 >= coordsItem[0] and posicion[2] <= coordsItem[0] + 45 and posicion[3] + 35 >= coordsItem[1] and posicion[3] <= coordsItem[1] + 20):
                        colisiony2 = False
                    #Colision Derecha y izquierda
                    if (posicion[2] + 45 >= coordsItem[0] and posicion[2] <= coordsItem[0] + 40 and posicion[1] + 35  >= coordsItem[1]  and posicion[1]  <= coordsItem[1] + 15):
                        colisionx1 = False
                    if (posicion[0] + 45 >= coordsItem[0] and posicion[0] <= coordsItem[0] + 40 and posicion[1] + 35  >= coordsItem[1]  and posicion[1]  <= coordsItem[1] + 15):
                        colisionx2 = False
                        
                if "VWall" in canva.gettags(item):
                    #Colision Derecha y izquierda
                    if (posicion[2] + 20 >= coordsItem[0] and posicion[2] <= coordsItem[0] + 10 and posicion[1] + 55  >= coordsItem[1]  and posicion[1]  <= coordsItem[1] + 15):
                        colisionx1 = False
                    if (posicion[0] + 10 >= coordsItem[0] and posicion[0] <= coordsItem[0] + 20 and posicion[1] + 55  >= coordsItem[1]  and posicion[1]  <= coordsItem[1] + 15):
                        colisionx2 = False
                        
                        
                    #Colision Arriba  y Abajo
                    if (posicion[0] + 20 >= coordsItem[0] and posicion[2] <= coordsItem[0] + 10 and posicion[1] <= coordsItem[1]  + 57  and posicion[1] + 45 >= coordsItem[1]):
                        colisiony1 = False
                    if (posicion[0] + 20 >= coordsItem[0] and posicion[2] <= coordsItem[0] + 10 and  posicion[3] + 55 >= coordsItem[1] and posicion[3] <= coordsItem[1] + 55):
                        colisiony2 = False
                
        
            if "w" in self.key and colisiony1:
                if posicion[1]<=100 or (posicion[0] + 35 >=  coordFountain[0] and posicion[2] <=  coordFountain[0] + 35 and posicion[1] <= coordFountain[1]  + 35  and posicion[1] + 35 >= coordFountain[1]):
                    y+=y  
                else:
                    y+=-self.speed
            elif "s" in self.key and colisiony2:
                if posicion[3]>=650 or (posicion[0] + 35 >= coordFountain[0] and posicion[2] <= coordFountain[0] + 35 and posicion[3] + 30 >= coordFountain[1] and posicion[3] <= coordFountain[1] + 30):
                    y-=y
                else:
                    y+=self.speed
            elif "d" in self.key and colisionx1:
                if posicion[2]>=967 or (posicion[2] + 35 >= coordFountain[0] and posicion[2] <= coordFountain[0] + 35 and posicion[1] + 20  >= coordFountain[1]  and posicion[1]  <= coordFountain[1] + 20):
                    x-=x
                else:
                    x+=self.speed
                    if self.frame > 11 or not "d" in self.key :
                        self.frame = 1
                    self.frame+=1
                    self.playerImg = cargarImagen("assets/CharacterSprites", f"Capa{self.frame}.png", 20, 30)
                    canva.itemconfig("pjSprite", image=self.playerImg)
            elif "a" in self.key and colisionx2:
                if posicion[0]<=25 or (posicion[0] + 35 >= coordFountain[0] and posicion[0] <= coordFountain[0] + 35 and posicion[1] + 20  >= coordFountain[1]  and posicion[1]  <= coordFountain[1] + 20):
                    x+=x
                else:
                    x-=self.speed
                    if self.frame >= 8 or not "a" in self.key :
                        self.frame = 1
                    self.frame+=1
                    self.playerImg = cargarImagen("assets/CharacterSprites", f"Left{self.frame}.png", 20, 30)
                    canva.itemconfig("pjSprite", image=self.playerImg)
                    
            
            canva.move(pj, x, y)
            canva.move("pjSprite", x, y)
            canva.update()
            canva.after(16, self.move, pj, canva)
        
        
    def pointsCounters(self, canva):
        self.points+=10
        canva.itemconfig("points", text="Points: " + str(self.points))
    

    
class Enemies:
    def __init__(self, x, y, speed, speedShoot, playerImg, hp):
        self.x = x
        self.y = y
        self.speed = speed
        self.speedShoot = speedShoot
        self.playerImg = playerImg
        self.hp = hp
    
    def draw(self, canva, cont):
        canva.create_rectangle(10, 20, 30, 50, fill="", outline="", tag="Enemy" + str(cont))
        canva.create_image(10, 20, image=self.playerImg, anchor="nw", tag="Enemy" + str(cont))
        canva.move("Enemy" + str(cont), self.x, self.y)
        canva.update()

    def hpAux(self, canva, enemy_tag, Player):
        balas = canva.find_withtag("balaPlayer")
        
        for bala in balas:
            bala_coords = canva.bbox(bala)
            if not bala_coords:
                continue

            overlapping = canva.find_overlapping(*bala_coords)
            
            for item in overlapping:
                if enemy_tag in canva.gettags(item):
                    if self.hp <= 1:
                        canva.delete(bala)
                        canva.delete(enemy_tag)
                        Player.pointsCounters(canva)
                        return
                    else:
                        self.hp -= 1
                        canva.delete(bala)
                        break  # para no seguir revisando esa bala
            
        canva.after(20, self.hpAux, canva, enemy_tag, Player)
    def enemyMove(self, canva, x, y, num, enemy):
        if canva.find_withtag(enemy):
            coordEnemy1 = canva.coords(enemy)
            overlapping = canva.find_overlapping(coordEnemy1[0]-15, coordEnemy1[1]-15, coordEnemy1[2]+15, coordEnemy1[3]+20)
            colisiony1 = True
            colisiony2 = True
            colisionx1 = True
            colisionx2 = True
            for item in overlapping:
                coordsItem = canva.coords(item)

                if "HWall" in canva.gettags(item):
                    #Colision Arriba  y Abajo
                    if (coordEnemy1[0] + 45 >= coordsItem[0] and coordEnemy1[2] <= coordsItem[0] + 45 and coordEnemy1[1] <= coordsItem[1]  + 47  and coordEnemy1[1] + 35 >= coordsItem[1]):
                        colisiony1 = False
                    if (coordEnemy1[0] + 45 >= coordsItem[0] and coordEnemy1[2] <= coordsItem[0] + 45 and coordEnemy1[3] + 35 >= coordsItem[1] and coordEnemy1[3] <= coordsItem[1] + 20):
                        colisiony2 = False
                    #Colision Derecha y izquierda
                    if (coordEnemy1[2] + 45 >= coordsItem[0] and coordEnemy1[2] <= coordsItem[0] + 40 and coordEnemy1[1] + 35  >= coordsItem[1]  and coordEnemy1[1]  <= coordsItem[1] + 15):
                        colisionx1 = False
                    if (coordEnemy1[0] + 45 >= coordsItem[0] and coordEnemy1[0] <= coordsItem[0] + 40 and coordEnemy1[1] + 35  >= coordsItem[1]  and coordEnemy1[1]  <= coordsItem[1] + 15):
                        colisionx2 = False
                        
                if "VWall" in canva.gettags(item):
                    #Colision Derecha y izquierda
                    if (coordEnemy1[2] + 20 >= coordsItem[0] and coordEnemy1[2] <= coordsItem[0] + 10 and coordEnemy1[1] + 55  >= coordsItem[1]  and coordEnemy1[1]  <= coordsItem[1] + 15):
                        colisionx1 = False
                    if (coordEnemy1[0] + 10 >= coordsItem[0] and coordEnemy1[0] <= coordsItem[0] + 20 and coordEnemy1[1] + 55  >= coordsItem[1]  and coordEnemy1[1]  <= coordsItem[1] + 15):
                        colisionx2 = False
                        
                        
                    #Colision Arriba  y Abajo
                    if (coordEnemy1[0] + 20 >= coordsItem[0] and coordEnemy1[2] <= coordsItem[0] + 10 and coordEnemy1[1] <= coordsItem[1]  + 57  and coordEnemy1[1] + 45 >= coordsItem[1]):
                        colisiony1 = False
                    if (coordEnemy1[0] + 20 >= coordsItem[0] and coordEnemy1[2] <= coordsItem[0] + 10 and  coordEnemy1[3] + 55 >= coordsItem[1] and coordEnemy1[3] <= coordsItem[1] + 55):
                        colisiony2 = False
                
            if canva.find_withtag(enemy):
                if num == 0 and colisionx2:
                    if coordEnemy1[0]<=30:
                        x+=x
                    else:
                        x-=20
                elif num == 1 and colisionx1:
                    if coordEnemy1[2]>=917:
                        x-=x
                    else:
                        x+=20
                elif num == 2 and colisiony2:
                    if coordEnemy1[3]>=630:
                        y-=y
                    else:
                        y+=20
                elif num == 3 and colisiony1:
                    if coordEnemy1[1]<=100:
                        y+=y
                    else:
                        y-=20
                canva.move(enemy, x, y)
                canva.update()
        canva.after(2000, self.enemyMove, canva, 0, 0, random.randint(0, 3), enemy)

    def enemyShoot(self, canva, enemy, imgBrokenHeart):
        if canva.find_withtag(enemy):
            x = canva.coords(enemy)[0]
            y = canva.coords(enemy)[1]
            xFinal = canva.coords("pj")[0]
            yFinal = canva.coords("pj")[1]
            bala = canva.create_oval(18, 10, 10, 18, fill="gray")
            
            distacia = round(math.sqrt((xFinal - x)**2 + (yFinal - y)**2))
            velocidadX = ((xFinal - x) / distacia) * self.speedShoot
            velocidadY = ((yFinal - y) / distacia) * self.speedShoot
            canva.move(bala, x, y)
            canva.update()
            self.enemyShootAux(canva, x, y, bala, 0, self.speedShoot, enemy, imgBrokenHeart, velocidadX, velocidadY)
        return
    
    def enemyShootAux(self, canva, xBala ,yBala, bala, metros, velocidad, enemy, imgBrokenHeart, velocidadX, velocidadY):
            
            if canva.find_withtag(bala) and not canva.find_withtag("breakFountain"):
                xFinal = canva.coords("pj")[0]
                yFinal= canva.coords("pj")[1]
                xFuente = canva.coords("fountain")[0]
                yFuente = canva.coords("fountain")[1]
                distaciaTiempoReal = round(math.sqrt((xFinal - xBala)**2 + (yFinal - yBala)**2))
                distaciaFuente = round(math.sqrt((xFuente - xBala)**2 + (yFuente - yBala)**2))
                balaCords = canva.coords(bala)
                overlapping = canva.find_overlapping(balaCords[0], balaCords[1], balaCords[2], balaCords[3])
                for item in overlapping:
                    if "HWall" in canva.gettags(item):
                        canva.delete(item)
                        canva.delete(bala)
                    elif "VWall" in canva.gettags(item):
                        canva.delete(item)
                        canva.delete(bala)
                if distaciaTiempoReal < 11:
                    canva.delete(bala)
                    if canva.find_withtag("heart1"):
                        canva.itemconfig("heart1", image=imgBrokenHeart, tag="broken1")
                    elif canva.find_withtag("heart2"):
                        canva.itemconfig("heart2", image=imgBrokenHeart, tag="broken2")
                    elif canva.find_withtag("heart3"):
                        canva.itemconfig("heart3", image=imgBrokenHeart, tag="broken3")
                    elif canva.find_withtag("heart4"):
                        canva.itemconfig("heart4", image=imgBrokenHeart, tag="broken4")
                    elif canva.find_withtag("heart5"):
                        canva.itemconfig("heart5", image=imgBrokenHeart, tag="broken5")
                        canva.create_text(520, 130, text="Game Over \n Please Press X For Try againg", font=('times', 30, 'bold'), fill="Red")
                        canva.delete("timer")
                        pygame.mixer.music.pause()
                        GameOver = pygame.mixer.Sound("assets/sounds/GameOver.mp3")
                        GameOver.set_volume(0.5)
                        GameOver.play()
                    return
                elif metros == 120:
                    canva.delete(bala)
                    return
                elif distaciaFuente < 40:
                    canva.create_text(520, 130, text="Game Over \n Please Press X For Try againg", font=('times', 30, 'bold'), fill="Red")
                    pygame.mixer.music.pause()
                    GameOver = pygame.mixer.Sound("assets/sounds/GameOver.mp3")
                    GameOver.set_volume(1.2)
                    GameOver.play()
                    destroy = pygame.mixer.Sound("assets/sounds/Fuente.mp3")
                    destroy.set_volume(0.1)
                    destroy.play()
                    canva.delete("timer")
                    destroyFountain = cargarImagen("assets/images/fountainFrames", "frame-02.png", 70, 70)
                    images.append(destroyFountain)
                    canva.itemconfig("fountain", image=destroyFountain, tag="breakFountain")
                    canva.delete(bala)
                    return
                canva.move(bala, velocidadX , velocidadY)
                canva.update()
            canva.after(20, self.enemyShootAux, canva, xBala + velocidadX, yBala + velocidadY, bala, metros + 1, velocidad, enemy, imgBrokenHeart, velocidadX, velocidadY)

    def visionZone(self, canva, enemy, imgBrokenHeart):
        if canva.find_withtag(enemy) and not canva.find_withtag("broken5") and  canva.find_withtag("pj") and not canva.find_withtag("breakFountain"):
            distancia = round(math.sqrt((canva.coords("pj")[0] - canva.coords(enemy)[0])**2 + (canva.coords("pj")[1] - canva.coords(enemy)[1])**2))
            if distancia < 200:
                self.enemyShoot(canva, enemy, imgBrokenHeart)
            canva.after(1000, self.visionZone, canva, enemy, imgBrokenHeart)
        else:
            return
        

            

        
