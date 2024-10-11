import os
import pygame
from settings import * 


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gunslingers Vengence')

#framerates
clock = pygame.time.Clock()

#moving/action booleans
movingLeft = False
movingRight = False
shoot = False

#images to load:
bulletIMG = pygame.image.load('IMG/Bullet/Small/0.png').convert_alpha()
bulletIMG = pygame.transform.scale(bulletIMG, (int(bulletIMG.get_width() * BULLET_SCALE) , (int(bulletIMG.get_height() * BULLET_SCALE))))
#draws background
def drawBG():
    screen.fill(BLACK)
    
    pygame.draw.line(screen, RED, (0,FLOOR), (SCREEN_WIDTH, 300))
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        super().__init__()
        self.speed = speed
        self.image = bulletIMG
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        self.rect.x += self.speed * self.direction


#creates sprite groups        
bulletGroup = pygame.sprite.Group()
        

#Gunslinger player class
class Gunslinger(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        
        self.speed = speed
        self.charType = charType
        self.direction = 1
        
        self.jump = False
        self.inAir = True
        
        self.velY = 0
        self.velX = 0
        
        self.flip = False
        self.animation_list = []
        self.frameIndex = 0
        
        #action value to indicate animation loop that plays
        self.action = 0
        
        self.updateTime = pygame.time.get_ticks()
        
        #load all images for players
        animationTypes = ['Idle', 'Walk', 'Jump/Normal', 'Jump/Gun']
        
        for animation in animationTypes:
            tempList = []
            
            #counts number of files in folder
            frameNum = len(os.listdir(f'IMG/{self.charType}/{animation}'))
        
            #handles idle animations
            for i in range(frameNum - 1):
                img = pygame.image.load(f'IMG/{self.charType}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale) , (int(img.get_height() * scale))))
                tempList.append(img)
                
            #appends idle tempList to overall animation list
            self.animation_list.append(tempList)

        #calls specific frame index based on action value 
        self.image = self.animation_list[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Create the mask for the player based on the current image
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, movingLeft, movingRight):
        #resets movment variables
        dx = 0
        dy = 0
        
        #assign movments for left and right
        if movingLeft:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            
        if movingRight:
            dx = self.speed
            self.flip = False
            self.direction = 1
            
        #assign jump movements
        if self.jump == True and self.inAir == False:
            self.velY = -20
            self.jump = False
            self.inAir = True
            
        #changes rate of change applies gravity    
        self.velY += GRAVITY
        
        if self.velY > 10:
            self.velY
            
        dy += self.velY
        
        if self.rect.bottom + dy > FLOOR:
            dy = FLOOR - self.rect.bottom
            self.inAir = False
            
        self.rect.x += dx
        self.rect.y += dy
    
    def updateAnimations(self):
        #update image based on current fram
        self.image = self.animation_list[self.action][self.frameIndex]
        #checks time since last update updates if enough time passed
        if pygame.time.get_ticks() - self.updateTime > ANIMATION_COOLDOWN:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
            
        #if animation runs out reset back to start
        if self.frameIndex >= len(self.animation_list[self.action]):
            self.frameIndex = 0;
            
        # Update the mask with the new image for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)
            
    def updateActions(self, newAction):
        #check if new action different from previous
        if newAction != self.action:
            self.action = newAction
            #reset animation loop to cater for new action
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
    


#initilization of players
player = Gunslinger('Cowboy', p_startX, p_startY, PLAYER_SCALE, PLAYER_SPEED)
enemy = Gunslinger('Gangster',400, 250, PLAYER_SCALE, PLAYER_SPEED)


run = True
while run:
    
    clock.tick()
    
    drawBG()
    
    
    player.updateAnimations()
    player.draw()
    enemy.updateAnimations()
    enemy.draw()
    
    #updates and draws groups
    bulletGroup.update()
    bulletGroup.draw(screen)
    
    #updates player actions
    if player.alive:
        if shoot:
            bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction, BULLET_SPEED)
            bulletGroup.add(bullet)
        if player.inAir:
            player.updateActions(2)
        elif movingLeft or movingRight:
            player.updateActions(1)#1 : walk
            
        #else if attacking: #create boolean value for attacking   
          
        else: 
            player.updateActions(0)#0: idle)
    
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
            
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_RETURN and player.alive:
                player.jump = True
            
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
            
            if event.key == pygame.K_SPACE:
                shoot = False     
    
    
    
    pygame.display.update()        

pygame.quit()