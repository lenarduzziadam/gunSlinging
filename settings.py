# -----------------------
# Level Configuration
# -----------------------
MAXLEVELS = 2  # Maximum number of levels in the game

# -----------------------
# Screen Dimensions
# -----------------------
SCREEN_WIDTH = 900  # Width of the game screen in pixels
SCREEN_HEIGHT = SCREEN_WIDTH * 0.8  # Height of the game screen based on aspect ratio

# Start and Exit button sizes and positions
SBUTTONSIZES_X = SCREEN_WIDTH // 2 - 130
SBUTTONSIZES_Y = SCREEN_HEIGHT // 2 - 150
EBUTTONSIZES_X = SCREEN_WIDTH // 2 - 110
EBUTTONSIZES_Y = SCREEN_HEIGHT // 2 + 50

# -----------------------
# Level and Tile Settings
# -----------------------
ROWS = 16  # Number of rows in each level
COLS = 150  # Number of columns in each level
TILESIZE = SCREEN_HEIGHT // ROWS  # Size of each tile based on screen height
TILETYPES = 21  # Number of tile types in the game

# Scrolling settings
SCROLLING_THRESHOLD = 300  # Distance from screen edge at which scrolling begins

# -----------------------
# Scale Settings for Visual Elements
# -----------------------
BG_SCALE = 2.1  # Scale factor for background images
PLAYER_SCALE = 1.4  # Scale factor for player sprites
DEATH_SCALE = 0.50  # Scale factor for death animation
HEALTH_SCALE = 1.8  # Scale factor for health icons
AMMO_SCALE = 1.2  # Scale factor for ammo icons

BULLET_SCALE = 0.02  # Scale factor for bullet sprites
CANNON_SCALE = 0.03  # Scale factor for cannonball sprites

# -----------------------
# Game Capabilities and Capacities
# -----------------------
CANNON_TIMER = 100  # Timer duration for cannon firing cooldown
X_ADJUST_BULLET = 0.28  # X-axis adjustment for bullet position
Y_ADJUST_BULLET = 0.25  # Y-axis adjustment for bullet position

PLAYER_HEALTH = 100  # Maximum health of the player character
ENEMY_HEALTH = 25  # Maximum health of enemies

PLAYER_AMMO = 100  # Maximum ammo capacity for the player
ENEMY_AMMO = 20  # Maximum ammo capacity for enemies

CANNON_AMMO = 25  # Maximum cannon ammo capacity

# -----------------------
# Health Bar Dimensions
# -----------------------
HB_LOC_X = 150  # Width of the health bar
HB_LOC_Y = 20  # Height of the health bar

# -----------------------
# Game Physics and Timings
# -----------------------
FPS = 40  # Frames per second limit
ANIMATION_COOLDOWN = 100  # Milliseconds between animation frames

GRAVITY = 0.70  # Gravity constant affecting the player’s velocity
VEL_LIMIT = 10  # Maximum vertical velocity limit
FLOOR = 420  # Height of the floor in the game
CANNON_VELOCITY = -12  # Initial velocity of the cannonball

EXPLOSIVE_RANGE = (TILESIZE * 2)  # Radius of explosion damage

# Timers and Explosion Settings
EXPLODE_CANNON_SCALE = 0.5  # Scale factor for explosion animation
BULLET_COOLDOWN = 40  # Cooldown time between bullets
CANNON_COOLDOWN = 150  # Cooldown time between cannon shots

# -----------------------
# Colors
# -----------------------
MPURPLE = (100, 20, 135)  # Custom purple color
BLACK = (0, 0, 0)  # Black color for background
GREEN = (0, 255, 0)  # Green color for UI elements or highlights
RED = (255, 0, 0)  # Red color for health or danger elements
WHITE = (255, 255, 255)  # White color for text or borders
BLUE = (25, 25, 200)  # Blue color for water elements
OFFBLACK = (23, 23, 23)  # Slightly lighter black
OFFWHITE = (254, 254, 254)  # Slightly off-white color

# -----------------------
# Layer Configuration
# -----------------------
PLAYER_LAYER = 4  # Layer index for the player character
ENEMY_LAYER = 3  # Layer index for enemies
BLOCK_LAYER = 2  # Layer index for obstacles and blocks
GROUND_LAYER = 1  # Layer index for the ground

# -----------------------
# Speed Settings for Characters and Projectiles
# -----------------------
PLAYER_SPEED = 2  # Speed of the player character
ENEMY_SPEED = 2  # Speed of enemy characters

BULLET_VELOCITY = (0, -350)  # Velocity of bullets when fired
BULLET_SPEED = 10  # Speed of bullets in the game
CANON_SPEED = 5  # Speed of cannonballs

EXPLOSION_SPEED = 4  # Speed of explosion animations

# -----------------------
# Vision Settings for AI
# -----------------------
VISION_VAR1 = 150  # Width of AI vision range
VISION_VAR2 = 20  # Height of AI vision range

# -----------------------
# Player Spawn Point
# -----------------------
p_startX = 200  # Starting X coordinate of the player
p_startY = 200  # Starting Y coordinate of the player


#Enviorment
home_map = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B.........................E..............E....B',
    'B....E................................EEEE....B',
    'B.................................E...........B',
    'B...........BBB...............................B',
    'B.............................................B',
    'B..........................................E..B',
    'B.....................P.......................B',
    'B..............................BBB............B',
    'B..........E...........................E......B',
    'B...................BBB.......................B',
    'B.............................................B',
    'B....B...............E....E..........B....E...B',
    'B............................................EB',
    'B.............................................B',
    'B.........................BBBBBB..............B',
    'B........BBBBBBB..............................B',
    'B.....................E.......................B',
    'B..................................E..........B',
    'B......................EE..........B..........B',
    'B.............................................B',
    'B.............E...............................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]


world_map = [
    '                                                                  ',
    '                                                                  ',
    '                t  t                                              ',
    '        X     XXXXXXXXXs                   XX   X                 ',
    ' tXXXt     XX         XX                XXXX tt XX                ',
    ' XX XX                                      XXXXX                 ',
    '          Xt    t           t  t   X                            G ',
    '        XXXXXX  XXXXs    XXXXXXXXXXX  XX              tt t     XXX',
    ' P   XX  X XX X  X XXXt     X XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
    'XXXXXXX  X  X X  X  XXXXXXXXX XX  XX  XXX  XX XX XXXXXXX  X       ',
]

tile_size = 50
WIDTH, HEIGHT = 1000, len(world_map) * tile_size


