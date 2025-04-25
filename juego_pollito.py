import pygame
import sys
import random


pygame.init()


ventana = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("¡Corre pollito!")


verde = (0, 255, 0)
gris = (46, 50, 46)
amarillo = (255, 255, 0)
rojo = (255, 0, 0)


reloj = pygame.time.Clock()

class Gallina(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))  
        self.image.fill(amarillo)
        self.rect = self.image.get_rect()
        self.rect.topleft = (460, 480)

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
        if teclas[pygame.K_UP]:
            self.rect.y -= 5
        if teclas[pygame.K_DOWN]:
            self.rect.y += 5

class Carro(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = pygame.Surface((40, 40)) 
        self.image.fill(rojo)
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
sprites = pygame.sprite.Group()
sprites.add(gallina)

sprites_car = pygame.sprite.Group()

def y_en_carretera(superior=True):
    if superior:
        return random.randint(250, 250 + 80 - 40)
    else:
        return random.randint(390, 390 + 80 - 40)


for i in range(10):
    
    x = random.randint(100, 1000)
    y = y_en_carretera(True)
    vel = random.randint(3, 6)
    sprites_car.add(Carro(x, y, vel))

    
    x = random.randint(0, 900)
    y = y_en_carretera(False)
    vel = -random.randint(3, 6)
    sprites_car.add(Carro(x, y, vel))

while True:

    reloj.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ventana.fill(verde)


    pygame.draw.rect(ventana, gris, (0, 250, 1000, 80))
    pygame.draw.rect(ventana, gris, (0, 390, 1000, 80))

    sprites.update()
    sprites.draw(ventana)

    sprites_car.update()
    sprites_car.draw(ventana)


    if pygame.sprite.spritecollideany(gallina, sprites_car):
        gallina.rect.topleft = (460, 480)

    pygame.display.flip()
    