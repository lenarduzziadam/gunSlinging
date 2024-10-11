import os
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
    
    pygame.draw.line(screen, RED, (0,FLOOR), (SCREEN_WIDTH, 300))
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, charType, pos, damage, scale):
        self.charType = charType
        self.animation_list = []
        self.frameIndex = 0
        
        tempList = []
        for i in range(4):
            BULLET = pygame.image.load(f'{charType}_{i}.png')
            BULLET = pygame.transform.scale(BULLET, (int(BULLET.get_width() * scale) , (int(BULLET.get_height() * scale))))
            self.image = BULLET
            tempList.append()
            
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(pos)
        
        self.vel = pygame.math.Vector2(BULLET_VELOCITY)
        self.damage = damage
        self.scale = scale
        
        
    def update(self, dt):
        
        self.pos += self.vel * dt
        self.rect.center = self.pos
        
        if self.rect.bottom <= 0:
            self.kill()

#Gunslinger player class
class Gunslinger(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        
        self.speed = speed
        self.charType = charType
        self.direction = 1
        self.jump = False
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
                img = pygame.image.load(f'IMG/{self.charType}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale) , (int(img.get_height() * scale))))
                tempList.append(img)
                
            #appends idle tempList to overall animation list
            self.animation_list.append(tempList)

        #calls specific frame index based on action value 
        self.image = self.animation_list[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        
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
        if self.jump == True:
            self.velY = -20
            self.jump = False
        
        #changes rate of change applies gravity    
        self.velY += GRAVITY
        
        if self.velY > 10:
            self.velY
            
        dy += self.velY
        
        if self.rect.bottom + dy > FLOOR:
            dy = FLOOR - self.rect.bottom
            
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
    
    #updates player actions
    if player.alive:
        if movingLeft or movingRight:
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
            
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
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
    
    
    
    pygame.display.update()        

pygame.quit()