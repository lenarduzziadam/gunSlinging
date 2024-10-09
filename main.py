import pygame
from settings import * 


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gunslingers Vengence')

#framerates
clock = pygame.time.Clock()

#moving booleans
movingLeft = False
movingRight = False

#draws background
def drawBG():
    screen.fill(BLACK)

#Gunslinger player class
class Gunslinger(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.charType = charType
        
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.index = 0
        
        for i in range(4):
            img = pygame.image.load(f'{self.charType}_{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale) , (int(img.get_height() * scale))))
            self.animation_list.append(img)

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        
    def move(self, movingLeft, movingRight):
        #resets movment variables
        dx = 0
        dy = 0
        #assign movments
        if movingLeft:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            
        if movingRight:
            dx = self.speed
            self.flip = False
            self.direction = 1
            
        self.rect.x += dx
        self.rect.y += dy
        
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
    


#initilization of players
player = Gunslinger('CowboyIMG/Cowboy4_idle with gun', p_startX, p_startY, PLAYER_SCALE, PLAYER_SPEED)
enemy = Gunslinger('EnemyIMG/Cowboy2_idle with gun',400, 250, PLAYER_SCALE, PLAYER_SPEED)


run = True
while run:
    
    clock.tick()
    
    drawBG()
    
    player.draw()
    enemy.draw()
    player.move(movingLeft, movingRight)

    for event in pygame.event.get():
        #quitting game
        if event.type == pygame.QUIT:
            run = False
            
        #keyboard presses
        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_LEFT:
                movingLeft = True        
            if event.key == pygame.K_RIGHT:
                movingRight = True
            
            if event.key == pygame.K_a:
                movingLeft = True        
            if event.key == pygame.K_d:
                movingRight = True
            
            if event.key == pygame.K_ESCAPE:
                run = False
        
        #keyboard release        
        if event.type == pygame.KEYUP:
        
            if event.key == pygame.K_LEFT:
                movingLeft = False
            if event.key == pygame.K_RIGHT:
                movingRight = False        
                
            if event.key == pygame.K_a:
                movingLeft = False
            if event.key == pygame.K_d:
                movingRight = False        
    
    
    
    pygame.display.update()        

pygame.quit()