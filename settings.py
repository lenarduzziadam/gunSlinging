#Sizes
SCREEN_WIDTH = 900;
SCREEN_HEIGHT = SCREEN_WIDTH * 0.8;

#LEVEL sizes
ROWS = 16
COLS = 150
TILESIZE = SCREEN_HEIGHT // ROWS;
TILETYPES = 21

#Scrolling aspects
SCROLLING_THRESHOLD = 300

#SCALES for levels
BG_SCALE = 2.1

PLAYER_SCALE = 2;

DEATH_SCALE = 0.75

HEALTH_SCALE = 1.8
AMMO_SCALE = 1.5

BULLET_SCALE = 0.02;
CANNON_SCALE = 0.03;

CANNON_TIMER = 100;

X_ADJUST_BULLET = 0.28 
Y_ADJUST_BULLET = 0.25

#Capcities (Health/Ammo, etc...)
PLAYER_HEALTH = 100
ENEMY_HEALTH = 25

PLAYER_AMMO = 100
ENEMY_AMMO = 20

CANNON_AMMO = 25

#Health BAR Config
HB_LOC_X = 150
HB_LOC_Y = 20

#Framerates
FPS = 40;
ANIMATION_COOLDOWN = 100

#Game Variables and Physics
GRAVITY = 0.70
VEL_LIMIT = 10
FLOOR = 420
CANNON_VELOCITY = -12

EXPLOSIVE_RANGE = (TILESIZE * 2)

#Timers/Explosion Scales
EXPLODE_CANNON_SCALE = 0.5

BULLET_COOLDOWN = 40
CANNON_COOLDOWN = 150

#Colors
MPURPLE = (100, 20, 135);
BLACK = (0, 0, 0);
GREEN = (0, 255, 0);
RED = (255, 0, 0);
WHITE = (255, 255, 255)
BLUE = (25, 25, 200)
OFFBLACK = (23, 23, 23)
OFFWHITE = (254, 254, 254)


#LAYER Classifications
PLAYER_LAYER = 4;
ENEMY_LAYER = 3;
BLOCK_LAYER = 2;
GROUND_LAYER = 1;

#SPEED Classifications
PLAYER_SPEED = 3;
ENEMY_SPEED = 2;

BULLET_VELOCITY = (0,-350);
BULLET_SPEED = 10;
CANON_SPEED = 5;

EXPLOSION_SPEED = 4;

#VISION config
VISION_VAR1 = 150
VISION_VAR2 = 20
#Player SPAWN POINT:
p_startX = 200
p_startY = 200

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


