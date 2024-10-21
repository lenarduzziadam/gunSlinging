#Author : Adam Lenarduzzi
#Project: Gunslinger game
#Genre: 2d platfomer with range wepaons

import os
import pygame, random, csv, button
from pygame import mixer
from settings import * 


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gunslingers Vengence')

#framerates
clock = pygame.time.Clock()

#scrolling
screenScroll = 0
bgScroll = 0

#LEVEL DEFINER
startGame = False
level = 1

#moving/action booleans
movingLeft = False
movingRight = False
shoot = False
cannon = False

cannonShot = False

#button images
startGameIMG = pygame.image.load('IMG/MainMenu/start.png').convert_alpha()
exitGameIMG = pygame.image.load('IMG/MainMenu/exit.png').convert_alpha()
retryIMG = pygame.image.load('IMG/MainMenu/retry.png').convert_alpha()

#background images
desertIMG = pygame.image.load('IMG/background/desert_BG.png')
desertIMG = pygame.transform.scale(desertIMG, (int(desertIMG.get_width() * BG_SCALE) , (int(desertIMG.get_height() * BG_SCALE))))

#images to load:
imageList = []
for x in range(TILETYPES):
    img = pygame.image.load(f'IMG/tile/{x}.png')
    img = pygame.transform.scale(img, (TILESIZE, TILESIZE))
    imageList.append(img)

bulletIMG = pygame.image.load('IMG/Bullet/Small/0.png').convert_alpha()
bulletIMG = pygame.transform.scale(bulletIMG, (int(bulletIMG.get_width() * BULLET_SCALE) , (int(bulletIMG.get_height() * BULLET_SCALE))))

cannonIMG = pygame.image.load('IMG/Bullet/Canon/0.png').convert_alpha()
cannonIMG = pygame.transform.scale(cannonIMG, (int(cannonIMG.get_width() * CANNON_SCALE),(int(cannonIMG.get_height() * CANNON_SCALE))))

healthIMG = pygame.image.load('IMG/Icons/Health/0.png').convert_alpha()
healthIMG = pygame.transform.scale(healthIMG, (int(healthIMG.get_width() * HEALTH_SCALE),(int(healthIMG.get_height() * HEALTH_SCALE))))

ammoIMG = pygame.image.load('IMG/Icons/Ammo/0.png').convert_alpha()
ammoIMG = pygame.transform.scale(ammoIMG, (int(ammoIMG.get_width() * AMMO_SCALE),(int(ammoIMG.get_height() * AMMO_SCALE))))

itemDrops = {
    'Health'    : healthIMG,
    'Ammo'      : ammoIMG
}

font = pygame.font.SysFont('Times New Roman', 30)

#music load in
pygame.mixer.music.load('Music/Lone.mp3')
pygame.mixer.music.play(-1, 0.0, 6000)


def drawText(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

#draws background
def drawBG():
    screen.fill(BLACK)
    width = desertIMG.get_width()
    screen.blit(desertIMG, ((0, 0)))

def resetLevel():
    enemyGroup.empty()
    bulletGroup.empty()
    itemDropsGroup.empty()
    decorationGroup.empty()
    waterGroup.empty()
    exitGroup.empty()
    
    #create empty tile list
    emptyData = []
    for row in range(ROWS):
        r = [-1] * COLS
        emptyData.append(r)
        
    return emptyData
        
#class to define world and level layout
class World():
    def __init__(self):
        self.obstacleList = []
    
    def processData(self, data):
        self.levelLength = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = imageList[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILESIZE
                    img_rect.y = y * TILESIZE
                    
                    tileData = (img, img_rect)
                    
                    if tile >= 0 and tile <= 8:
                        self.obstacleList.append(tileData)
                        
                    elif tile >= 9 and tile <= 10:
                        water = Aqua(img, x * TILESIZE, y * TILESIZE)
                        waterGroup.add(water) 
                    
                    elif tile >= 11 and tile <= 14:
                        decoration = Decorative(img, (int(x * TILESIZE)), (int(y * TILESIZE)))
                        decorationGroup.add(decoration) 
                    
                    elif tile == 15: 
                        #initilization of players
                        player = Gunslinger('Cowboy', x * TILESIZE, y * TILESIZE, PLAYER_SCALE, PLAYER_SPEED, PLAYER_AMMO, PLAYER_HEALTH, 0)
                        healthbar = HealthBar(10, 10, player.health, player.health)

                    elif tile == 16:
                        enemy = Gunslinger('Gangster', x * TILESIZE, y * TILESIZE, PLAYER_SCALE, ENEMY_SPEED, ENEMY_AMMO, ENEMY_HEALTH, 0)    
                        enemyGroup.add(enemy)   
                        
                    elif tile == 17:
                        ammoBox = ItemDrops('Ammo', x * TILESIZE, y * TILESIZE)
                        itemDropsGroup.add(ammoBox) 
                    
                    elif tile == 18: #TODO: Implement Cannonball stuff and explosions
                        pass
                        
                    elif tile == 19:
                        healthHeart = ItemDrops('Health', x * TILESIZE, y * TILESIZE)
                        itemDropsGroup.add(healthHeart) 
                    
                    elif tile == 20: #creates exit
                        exit = Exit(img, (int(x * TILESIZE)), (int(y * TILESIZE)))
                        exitGroup.add(exit) 
    
        #returns player and healthbar making it global
        return player, healthbar              
                                                    
    
    def draw(self):
        for tile in self.obstacleList:
            tile[1][0] += screenScroll
            screen.blit(tile[0], tile[1])

#class for decorative objects
class Aqua(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = ((int(x + TILESIZE // 2)), (int(y + (TILESIZE - self.image.get_height()))))

    def update(self):
        self.rect.x += screenScroll
        
#class for decorative objects
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = ((int(x + TILESIZE // 2)), (int(y + (TILESIZE - self.image.get_height()))))

    def update(self):
        self.rect.x += screenScroll

#class for decorative objects
class Decorative(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.midtop = ((int(x + TILESIZE // 2)), (int(y + (TILESIZE - self.image.get_height()))))
    
    def update(self):
        self.rect.x += screenScroll
                                                   
#Implementation for item drops
class ItemDrops(pygame.sprite.Sprite):
    def __init__(self, itemType, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.itemType = itemType
        
        #item drops
        self.image = itemDrops[self.itemType]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))
    
    def update(self):
        
        self.rect.x += screenScroll
        
        #checks for player collision with box then adds to health/inventory
        if pygame.sprite.collide_mask(self, player):
            #checks box itemType
            if self.itemType == 'Health':
                player.health += 25
                
                #check to ensure health does not go over max
                if player.health > player.maxHealth:
                    player.health = player.maxHealth
                
                print(f'Feel the Love picked up a Southern Heart \nPlayer Health: {player.health}')
                    
            elif self.itemType == 'Ammo': 
                player.ammo += 10
                print(f'Picked up Ammo box!\nPlayer Ammo now: {player.ammo}')
                
            #deletes item box
            self.kill()

#making class for health bar
class HealthBar():
    def __init__(self, x, y, health, maxHealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxHealth = maxHealth
        
    def draw(self, health):
        #updates health
        self.health = health
        
        #health ratio calculation
        ratio = self.health/self.maxHealth
        
        pygame.draw.rect(screen, OFFBLACK, (self.x - 3, self.y - 3, HB_LOC_X + 5, HB_LOC_Y + 5))
        pygame.draw.rect(screen, RED, (self.x, self.y, HB_LOC_X, HB_LOC_Y))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, HB_LOC_X * ratio, HB_LOC_Y))            
            
#TODO: Explosion class needs to be fully implemented (and files/animations need to be added) 
#Also needs method for animation updates
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        
        self.scale = scale
        self.explosion_list = []
        self.frameIndex = 0
        self.explode = 0
        
        #action value to indicate animation loop that plays
        #self.explosion = 0
        
        self.updateTime = pygame.time.get_ticks()
        
        #load all images for players
        explosionTypes = ['Cannon', 'Nitroglycerin', 'Dynamite']
        
        for explosion in explosionTypes:
            tempList = []
        
            explosionFrameNum = len(os.listdir(f'IMG/Explosives/{explosion}'))
            
            #for loop meant to iterate through animations for explosions 
            for num in range(explosionFrameNum):
                explosionIMG = pygame.image.load(f'IMG/Explosives/{explosion}/{num}.png').convert_alpha()
            
                explosionIMG = pygame.transform.scale(explosionIMG, (int(explosionIMG.get_width() * scale) , (int(explosionIMG.get_height() * scale))))
                #appends images to templist
                tempList.append(explosionIMG)
                
            #appends idle tempList to overall animation list
            self.explosion_list.append(tempList)
                
        self.image = self.explosion_list[self.explosion][self.frameIndex]
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        
        # Create the mask for the explosion on the current image
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        #updates explosion animations
        self.counter += 1
        
        if self.counter >= EXPLOSION_SPEED:
            self.count = 0
            self.frameIndex += 1
            
            #checks if animation complete
            if self.frameIndex >= len(self.explosion_list):
                self.kill()     
            else:
                self.image = self.explosion_list[self.frameIndex]
                
    def updateAnimations(self):
        #update image based on current fram
        self.image = self.explosion_list[self.explode][self.frameIndex]
        #checks time since last update updates if enough time passed
        if pygame.time.get_ticks() - self.updateTime > ANIMATION_COOLDOWN:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
            
        #if animation runs out reset back to start
        if self.frameIndex >= len(self.animation_list[self.explode]):
            self.frameIndex = len(self.animation_list[self.explode]) - 1
        
        # Update the mask with the new image for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)
                
    def updateExplosions(self, newExplosion):
        #check if new action different from previous
        if newExplosion != self.explode:
            self.explode = newExplosion
            #reset animation loop to cater for new action
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()
            
class Cannonball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        super().__init__()
        self.timer = CANNON_TIMER
        self.velY = CANNON_VELOCITY
        self.speed = speed
        self.image = cannonIMG
        
        # Flip the bullet horizontally if the direction is negative (facing left)
        if player.direction == -1:  #KEY: -1 is left, 1 is right
            self.image = pygame.transform.flip(self.image, True, False)
        
            #Regenerate the mask after updating the image
            self.mask = pygame.mask.from_surface(self.image)
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
        # Create a mask for the bullet based on its image
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.velY += GRAVITY
        dx = self.direction * self.speed
        dy = self.velY
        
        
        if self.rect.bottom + dy > FLOOR:
            dy = FLOOR - self.rect.bottom
            self.speed = self.speed/2
            
        #checks if bullet off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        #updates cannonball position
        self.rect.x += dx
        self.rect.y += dy
        
        #countdown timer
        if self.timer <=0:
            self.kill()
            explode = Explosion(self.rect.x, self.rect.y, EXPLODE_CANNON_SCALE)
            explosionGroup.add(explode)
            
            #do damage to anything nearby
            if abs(self.rect.centerx - player.rect.centerx) < EXPLOSIVE_RANGE and \
                abs(self.rect.centery - player.rect.centery) < EXPLOSIVE_RANGE:
                player.health -= 30
            
            for enemy in enemyGroup:
                if abs(self.rect.centerx - enemy.rect.centerx) < EXPLOSIVE_RANGE and \
                    abs(self.rect.centery - enemy.rect.centery) < EXPLOSIVE_RANGE:
                    player.health -= 30
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, owner, x, y, direction, speed):
        super().__init__()
        self.speed = speed
        self.image = bulletIMG
        self.owner = owner
        
        # Flip the bullet horizontally if the direction is negative (facing left)
        if owner.direction == -1:  #KEY: -1 is left, 1 is right
            self.image = pygame.transform.flip(self.image, True, False)
            # Always regenerate the mask after updating the image
            self.mask = pygame.mask.from_surface(self.image)
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
        # Create a mask for the bullet based on its image
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect.x += (self.speed * self.direction)

        #checks if bullet off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        for tile in world.obstacleList:
            if tile[1].colliderect(self.rect):
                self.kill()

        #section added to avoid friendly fire with player characters own weapon
        if self.owner != player:
            #collision checks
            if pygame.sprite.spritecollide(player, bulletGroup, False, pygame.sprite.collide_mask):
                if player.alive:
                    print(f"Player hit by enemy bullet! HP: {player.health}")
                    player.health -= 5
                    self.kill()
        
        #setting to avoid friendly fire amongst enemies            
        
        for enemy in enemyGroup:
            if self.owner != enemy:           
                if pygame.sprite.spritecollide(enemy, bulletGroup, False, pygame.sprite.collide_mask):
                    if enemy.alive:
                        print(f"Enemy hit by player bullet! Enemy HP:{enemy.health}")
                        enemy.health -= 5
                        self.kill()
            
#Gunslinger player class
class Gunslinger(pygame.sprite.Sprite):
    def __init__(self, charType, x, y, scale, speed, ammo, health, balls = 0):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        
        self.speed = speed
        
        self.shootCooldown = 0
        self.cannonCooldown = 0
        
        self.ammo = ammo
        self.startAmmo = ammo
        self.balls = balls
        self.health = health
        self.maxHealth = self.health
        
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
        
        #ai specific Variables
        self.moveCounter = 0
        self.vision = pygame.Rect(0, 0, VISION_VAR1, VISION_VAR2)
        self.idling = False
        self.idleCounter = 0
        
        
        #load all images for players
        animationTypes = ['Idle', 'Walk', 'Jump/Normal', 'Jump/Gun', 'Shoot', 'Death']
        
        for animation in animationTypes:
            tempList = []
            
            #counts number of files in folder
            frameNum = len(os.listdir(f'IMG/{self.charType}/{animation}'))
        
            #handles idle animations
            for i in range(frameNum - 1):
                img = pygame.image.load(f'IMG/{self.charType}/{animation}/{i}.png').convert_alpha()
               
                if animation == 'Death':
                    img = pygame.transform.scale(img, (int(img.get_width() * DEATH_SCALE) , (int(img.get_height() * DEATH_SCALE))))
                    #continue
                else:
                    img = pygame.transform.scale(img, (int(img.get_width() * scale) , (int(img.get_height() * scale))))
                
                #appends images to templist
                tempList.append(img)
                
            #appends idle tempList to overall animation list
            self.animation_list.append(tempList)

        #calls specific frame index based on action value 
        self.image = self.animation_list[self.action][self.frameIndex]
        
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.mask = pygame.mask.from_surface(self.image)
        self.width, self.height = self.mask.get_size()

        self.width = self.width * 3 // 5  # Adjusting width as needed
        self.height = self.height - 2      # Adjusting height as needed
        
    def update(self):
        self.updateAnimations()
        self.checkAlive()
        #update shootCooldown
        if self.shootCooldown > 0:
            self.shootCooldown -= 1;
        
        #updates cannon cooldown MAY or May not use
        if self.cannonCooldown > 0:
            self.cannonCooldown -= 1;   
                       
            
    def move(self, movingLeft, movingRight):
        #resets movment variables
        screenScroll = 0
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
        
        #checks for collision
        for tile in world.obstacleList:
            
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            
            #check for collision in y axis
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below ground
                if self.velY < 0:
                    self.velY = 0
                    dy = tile[1].bottom - self.rect.top
                    
                elif self.velY >=0:
                    self.velY = 0
                    self.inAir = False
                    dy = tile[1].top - self.rect.bottom
                    
        if pygame.sprite.spritecollide(self, waterGroup, False):
            self.health -=1
        
        #exit behavior
        levelComplete = False    
        if pygame.sprite.spritecollide(self, exitGroup, False):
            levelComplete = True
            
        #checks if fell off map            
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health -= 25
        
        #check if going off edge
        if self.charType == 'Cowboy' and self.alive:
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0    
            
        self.rect.x += dx
        self.rect.y += dy
        
        #update scroll based on player. 
        if self.charType == 'Cowboy' and self.alive:
            if (self.rect.right > (SCREEN_WIDTH - SCROLLING_THRESHOLD) and movingRight) or (self.rect.left < level_width - SCROLLING_THRESHOLD):
                self.rect.x -= dx
                screenScroll = -dx
            
                
        return screenScroll, levelComplete;
    
    def shoot(self, int1 = X_ADJUST_BULLET, int2 = Y_ADJUST_BULLET):
        self.int1 = int1
        self.int2 = int2
        
        if self.shootCooldown == 0 and self.ammo > 0:
            self.shootCooldown = BULLET_COOLDOWN
            bullet = Bullet(self, self.rect.centerx + (self.int1 * self.rect.size[0] * self.direction), self.rect.centery + (self.int2 * self.rect.size[0]), self.direction, BULLET_SPEED)
            bulletGroup.add(bullet)
            
            #ammo reduction
            self.ammo -= 1
            
    def ai(self):
        if self.alive:
        
            if self.idling == False and random.randint(1, 300) == 1:
                self.idling = True
                self.idleCounter = 420
            
            #check if ai is near player then shoots if close by
            if self.vision.colliderect(player.rect) and player.alive:
                self.updateActions(4)
                self.shoot()
                    
            elif self.idling == False:
                if self.direction == 1:
                    aiMovesRight = True
                else:
                    aiMovesRight = False
                
                aiMovesLeft = not aiMovesRight
                
                self.move(aiMovesLeft, aiMovesRight)
                 
                self.updateActions(1)#1 : walk  
                
                self.moveCounter += 1
                
                #updates vision counter rect as enemy moves
                self.vision.center = (self.rect.centerx + (VISION_VAR1/2) * self.direction, self.rect.centery)
                
                if self.moveCounter > TILESIZE:
                    self.direction *= -1
                    self.moveCounter *= -1
            
            else:
                #fixed issue here
                if self.idling == True:
                    self.updateActions(0)#0 : idle
                    self.idleCounter -= 1
                if self.idleCounter < 0:
                    self.idling = False
                    
        self.rect.x += screenScroll
    
    #CLASS DESIGNATED FOR CANNON #MIGHT NEED to be put in seperate class        
    def cannon(self, int1, int2):
        self.int1 = int1
        self.int2 = int2
        
        if self.balls > 0 and self.cannonCooldown == 0:
            self.cannonCooldown = CANNON_COOLDOWN
            cannonball = Cannonball(self.rect.centerx + (self.int1 * self.rect.size[0] * self.direction), self.rect.centery + (self.int2 * self.rect.size[0]), self.direction, CANON_SPEED)
            cannonGroup.add(cannonball)
            
            self.balls -= 1
            
        
    def updateAnimations(self):
        #update image based on current fram
        self.image = self.animation_list[self.action][self.frameIndex]
        #checks time since last update updates if enough time passed
        if pygame.time.get_ticks() - self.updateTime > ANIMATION_COOLDOWN:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
            
        #if animation runs out reset back to start
        if self.frameIndex >= len(self.animation_list[self.action]):
            
            if self.action == 5: #checks for Death animation loop and ends it at last animation
                self.frameIndex = len(self.animation_list[self.action]) - 1
                
            else:
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

    def checkAlive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.updateActions(5)
            
        
    def draw(self, display_mask=False):
        # Draw player sprite
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
        # If display_mask is True, visualize the mask
        if display_mask:
            mask_surface = self.mask.to_surface(setcolor=(0, 255, 0), unsetcolor=(0, 0, 0))
            screen.blit(mask_surface, self.rect.topleft)

#creating buttons
startButton = button.Button(SBUTTONSIZES_X, SBUTTONSIZES_Y, startGameIMG, 1)    
exitButton = button.Button(EBUTTONSIZES_X, EBUTTONSIZES_Y, exitGameIMG, 1) 
retryButton = button.Button(SBUTTONSIZES_X, SBUTTONSIZES_Y, retryIMG, 1)
         
#creates sprite groups        
bulletGroup = pygame.sprite.Group()
cannonGroup = pygame.sprite.Group()        
explosionGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()    
itemDropsGroup = pygame.sprite.Group()
waterGroup = pygame.sprite.Group()
exitGroup = pygame.sprite.Group()
decorationGroup = pygame.sprite.Group()


#create empty tile list
worldData = []
for row in range(ROWS):
    r = [-1] * COLS
    worldData.append(r)

# Loads level data to create world
with open(f'Levels/level{level}_data.csv', newline='') as csvfile:  # Fix applied here
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            worldData[x][y] = int(tile)

world = World()
player, healthbar = world.processData(worldData)
# Calculate the level width based on the processed data
level_width = world.levelLength * TILESIZE

run = True
while run:
    
    clock.tick()
    
    if startGame == False:
        #draw menu
        screen.fill(GREEN)
        
        if startButton.draw(screen):
            startGame = True
        if exitButton.draw(screen):
            run = False
    else:
    
        drawBG()
        
        #draws world map
        world.draw()
        
        healthbar.draw(player.health)
        drawText(f'AMMO: {player.ammo}', font, WHITE, 10, 35)
        

        player.update()
        player.draw()
        
        for enemy in enemyGroup:
            enemy.ai()
            enemy.update()
            enemy.draw()
        
        #updates and draws groups
        bulletGroup.update()
        bulletGroup.draw(screen)
        itemDropsGroup.update()
        itemDropsGroup.draw(screen)
        waterGroup.update()
        decorationGroup.update()
        exitGroup.update()
        waterGroup.draw(screen)
        exitGroup.draw(screen)
        decorationGroup.draw(screen)
        
    
        #updates player actions
        if player.alive:
                
            if player.inAir:
                if shoot:
                    #TODO: Does not seem to run figure out why
                    player.updateActions(3)#3:Jumping shooting animation
                    player.shoot(X_ADJUST_BULLET, Y_ADJUST_BULLET)
                else:
                    player.updateActions(2)
                    
            elif shoot and not (movingLeft or movingRight):
                player.updateActions(4)#4: standing/walking shooting animation
                player.shoot(X_ADJUST_BULLET, Y_ADJUST_BULLET)  
                    
            elif movingLeft or movingRight:
                player.updateActions(1)#1 : walk  
                
            else: 
                player.updateActions(0)#0: idle)
        
            screenScroll, levelComplete = player.move(movingLeft, movingRight)
        
        else:
            screenScroll = 0
            if retryButton.draw(screen):
                worldData = resetLevel()    
                
                # Loads level data to create world
                with open(f'Levels/level{level}_data.csv', newline='') as csvfile:  # Fix applied here
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            worldData[x][y] = int(tile)
            
                world = World()
                player, healthbar = world.processData(worldData)
                        
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