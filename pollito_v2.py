import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("¡Corre pollito!")

verde = (0, 255, 0)
gris = (46, 50, 46)
amarillo = (255, 255, 0)
rojo = (255, 0, 0)
blanco = (255, 255, 255)
color_anden = (122, 128, 122)

# Cargar imágenes
carro_azul = pygame.image.load("img/carro_azul.png")
carro_azul = pygame.transform.scale(carro_azul, (30, 30))
carro_gris = pygame.image.load("img/Carro_gris.png")
carro_gris = pygame.transform.scale(carro_gris, (30, 30))
porche = pygame.image.load("img/porche.png")
porche = pygame.transform.scale(porche, (30, 30))
pollo = pygame.image.load("img/pollo.png")
pollo = pygame.transform.scale(pollo, (40, 40))
carro_rojo = pygame.image.load("img/carro_rojo.png")
carro_rojo = pygame.transform.scale(carro_rojo, (40, 40))
casa = pygame.image.load("img/casa.png")
casa = pygame.transform.scale(casa, (70, 70))
pygame.mixer.music.load("sounds/autopista.ogg")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.5)
son_pollo = pygame.mixer.Sound("sounds/pollo.ogg")
choque = pygame.mixer.Sound("sounds/choque.ogg")

reloj = pygame.time.Clock()
fuente_arial = pygame.font.SysFont("arial", 30, 1, 1)

vidas = 3

class Gallina(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pollo  
        self.rect = self.image.get_rect()
        self.rect.topleft = (460, 480)
        self.pun = 0
        self.zona_segura = False
        self.ultimo_sonido = 0 

    def update(self):
        teclas = pygame.key.get_pressed()
        tiempo_actual = pygame.time.get_ticks()

        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
            if tiempo_actual - self.ultimo_sonido > 200:
                son_pollo.play()
                self.ultimo_sonido = tiempo_actual

        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
            if tiempo_actual - self.ultimo_sonido > 200:
                son_pollo.play()
                self.ultimo_sonido = tiempo_actual

        if teclas[pygame.K_UP]:
            self.rect.y -= 5
            if tiempo_actual - self.ultimo_sonido > 200:
                son_pollo.play()
                self.ultimo_sonido = tiempo_actual

        if teclas[pygame.K_DOWN]:
            self.rect.y += 5
            if tiempo_actual - self.ultimo_sonido > 200:
                son_pollo.play()
                self.ultimo_sonido = tiempo_actual

        if self.rect.y < 200 and not self.zona_segura:
            self.pun += 1
            self.zona_segura = True
        elif self.rect.y > 470 and self.zona_segura:
            self.pun += 1
            self.zona_segura = False

    def puntos(self): 
        ventana.blit(fuente_arial.render(f"Puntos = {self.pun}", True, blanco), (650, 25))

class Carro(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = random.choice([carro_gris, carro_azul, porche, carro_rojo]) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = velocidad

    def update(self):
        self.rect.x += self.velocidad
        if self.velocidad > 0 and self.rect.left > 1000:
            self.rect.right = 0
        elif self.velocidad < 0 and self.rect.right < 0:
            self.rect.left = 1000

# Crear instancias
gallina = Gallina()
sprites = pygame.sprite.Group(gallina)
sprites_car = pygame.sprite.Group()

def y_en_carretera(superior=True):
    if superior:
        return random.choice([250, 290])
    else:
        return random.choice([390, 430])

for i in range(10):
    x = random.randint(100, 1000)
    y = y_en_carretera(True)
    vel = -6
    sprites_car.add(Carro(x, y, vel))

    x = random.randint(0, 900)
    y = y_en_carretera(False)
    vel = 6
    sprites_car.add(Carro(x, y, vel))

# Bucle principal
while True:
    reloj.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ventana.fill(verde)

    # Dibujar pistas y andenes
    pygame.draw.rect(ventana, gris, (0, 250, 1000, 80))
    pygame.draw.rect(ventana, gris, (0, 390, 1000, 80))
    pygame.draw.rect(ventana, color_anden, (0, 200, 1000, 50))
    pygame.draw.rect(ventana, color_anden, (0, 470, 1000, 50))

    # Casas
    ventana.blit(casa, (0, 5))
    ventana.blit(casa, (500, 10))
    ventana.blit(casa, (60, 600))
    ventana.blit(casa, (500, 625))
    ventana.blit(casa, (600, 600))
 
    ventana.blit(fuente_arial.render(f"Vidas = {vidas}", True, blanco), (850, 25))

    sprites.update()
    gallina.puntos()
    sprites.draw(ventana)

    sprites_car.update()
    sprites_car.draw(ventana)
    
    if pygame.sprite.spritecollideany(gallina, sprites_car):
        vidas -= 1
        choque.play()
        gallina.rect.topleft = (460, 470)

    if vidas <= 0:
        ventana.blit(fuente_arial.render("GAME OVER", True, blanco), (450, 325))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    pygame.display.flip()
