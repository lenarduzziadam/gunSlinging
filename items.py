
import pygame, os
from settings import * 


healthIMG = pygame.image.load('IMG/Bullet/Canon/0.png').convert_alpha()
healthIMG = pygame.transform.scale(healthIMG, (int(healthIMG.get_width() * HEALTH_SCALE),(int(healthIMG.get_height() * HEALTH_SCALE))))

#Implementation for item drops
class ItemDrops(pygame.sprite.Sprite):
    def __init__(self, itemType, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.itemType = itemType
        
        #item drops
        self.image = itemDrops[self.itemType]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))
        