import pygame as pg
vec = pg.math.Vector2

# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BRIGHTBROWN = (87, 77, 51)
CYAN = (109, 221, 207)

# Game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BRIGHTBROWN
MUSIC_VOLUME = 0.5
SOUNDS_VOLUME = 0.4

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'soldier1_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 400
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEEDS = [200, 180, 160, 140, 120]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 40
DETECT_RADIUS = 400

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATION = 40
BLOOD_SPLASHES_RED = ['bloodsplats_0003.png', 'bloodsplats_0004.png', 'bloodsplats_0006.png']
BLOOD_SPLASHES_GREEN = ['bloodZ_0003.png', 'bloodZ_0004.png', 'bloodZ_0006.png']
BLOOD_DURATION = 20000

# Layers
WALL_LAYER = 1
BLOOD_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4

# Items
ITEM_IMAGES = {'Health': 'health_pack.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.3

# Sounds
#'Kim.WeLeft.ogg'#
BG_MUSIC = ['City.ogg', 'Myst.ogg', 'Road.ogg']
PLAYER_HIT_SOUNDS = ['pain1.wav', 'pain2.wav', 'pain3.wav', 'pain4.wav']
ZOMBIE_MOAN_SOUNDS = ['zombie_moan1.wav', 'zombie_moan2.wav', 'zombie_moan3.wav', 'zombie_moan4.wav']
ZOMBIE_HIT_SOUNDS = ['zombie_hit1.wav', 'zombie_hit2.wav', 'zombie_hit3.wav', 'zombie_hit4.wav', 'zombie_hit5.wav']
WEAPON_SOUNDS_GUN = ['pistol.wav']
EFFECT_SOUNDS = {'health_up': 'health_pick.wav'}
