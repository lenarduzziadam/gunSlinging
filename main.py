import pygame
from settings import * 


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gunslingers Vengence')

#Gunslinger player class
class Gunslinger(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('CowboyIMG/Cowboy4_idle with gun_0.png')

        self.image = pygame.transform.scale(img, (int(img.get_width() * scale) , (int(img.get_height() * scale))))

        self.rect = self.image.get_rect()
        self.rect.center = (x, x)

player = Gunslinger(p_startX, p_startY, PLAYER_SCALE)
player2 = Gunslinger(400, 250, PLAYER_SCALE)

run = True
while run:
    
    screen.blit(player.image, player.rect)
    screen.blit(player2.image, player2.rect)
    
    
    for event in pygame.event.get():
        #quitting game
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()        

pygame.quit()