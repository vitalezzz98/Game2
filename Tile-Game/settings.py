import pygame as pg
from random import choice
vec = pg.math.Vector2

# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (131, 0, 0)
YELLOW = (255, 255, 0)
BRIGHTBROWN = (87, 77, 51)
CYAN = (109, 221, 207)

# Game settings
#WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
#HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Tilemap Demo"
MENU_IMAGE = 'menu1.png'
BGCOLOR = BRIGHTBROWN
MUSIC_VOLUME = 0.5
SOUNDS_VOLUME = 0.4

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IDLE_IMG = ['surv_idle (1).png', 'surv_idle (2).png', 'surv_idle (3).png', 'surv_idle (4).png', 'surv_idle (5).png', 'surv_idle (6).png',
                    'surv_idle (7).png', 'surv_idle (8).png', 'surv_idle (9).png', 'surv_idle (10).png', 'surv_idle (11).png', 'surv_idle (12).png',
                    'surv_idle (13).png', 'surv_idle (14).png', 'surv_idle (15).png', 'surv_idle (16).png', 'surv_idle (17).png', 'surv_idle (18).png',
                    'surv_idle (19).png', 'surv_idle (20).png',]
PLAYER_MOVE_IMG = ['surv_move (1).png', 'surv_move (2).png', 'surv_move (3).png', 'surv_move (4).png', 'surv_move (5).png', 'surv_move (6).png',
                    'surv_move (7).png', 'surv_move (8).png', 'surv_move (9).png', 'surv_move (10).png', 'surv_move (11).png', 'surv_move (12).png',
                    'surv_move (13).png', 'surv_move (14).png', 'surv_move (15).png', 'surv_move (16).png', 'surv_move (17).png', 'surv_move (18).png',
                    'surv_move (19).png', 'surv_move (20).png',]
PLAYER_SHOOT_IMG = ['surv_shoot (1).png', 'surv_shoot (2).png', 'surv_shoot (3).png']
PLAYER_RELOAD_IMG = ['surv_reload (1).png', 'surv_reload (2).png', 'surv_reload (3).png', 'surv_reload (4).png', 'surv_reload (5).png', 'surv_reload (6).png',
                    'surv_reload (7).png', 'surv_reload (8).png', 'surv_reload (9).png', 'surv_reload (10).png', 'surv_reload (11).png', 'surv_reload (12).png',
                    'surv_reload (13).png', 'surv_reload (14).png', 'surv_reload (15).png']
PLAYER_SHOTGUN_IDLE_IMG = ['surv_shot_idle (1).png', 'surv_shot_idle (2).png', 'surv_shot_idle (3).png', 'surv_shot_idle (4).png', 'surv_shot_idle (5).png', 'surv_shot_idle (6).png',
                    'surv_shot_idle (7).png', 'surv_shot_idle (8).png', 'surv_shot_idle (9).png', 'surv_shot_idle (10).png', 'surv_shot_idle (11).png', 'surv_shot_idle (12).png',
                    'surv_shot_idle (13).png', 'surv_shot_idle (14).png', 'surv_shot_idle (15).png', 'surv_shot_idle (16).png', 'surv_shot_idle (17).png', 'surv_shot_idle (18).png',
                    'surv_shot_idle (19).png', 'surv_shot_idle (20).png',]
PLAYER_SHOTGUN_MOVE_IMG = ['surv_shot_move (1).png', 'surv_shot_move (2).png', 'surv_shot_move (3).png', 'surv_shot_move (4).png', 'surv_shot_move (5).png', 'surv_shot_move (6).png',
                    'surv_shot_move (7).png', 'surv_shot_move (8).png', 'surv_shot_move (9).png', 'surv_shot_move (10).png', 'surv_shot_move (11).png', 'surv_shot_move (12).png',
                    'surv_shot_move (13).png', 'surv_shot_move (14).png', 'surv_shot_move (15).png', 'surv_shot_move (16).png', 'surv_shot_move (17).png', 'surv_shot_move (18).png',
                    'surv_shot_move (19).png', 'surv_shot_move (20).png',]
PLAYER_SHOTGUN_SHOOT_IMG = ['surv_shot_shoot (1).png', 'surv_shot_shoot (2).png', 'surv_shot_shoot (3).png']
PLAYER_SHOTGUN_RELOAD_IMG = ['surv_shot_reload (1).png', 'surv_shot_reload (2).png', 'surv_shot_reload (3).png', 'surv_shot_reload (4).png', 'surv_shot_reload (5).png', 'surv_shot_reload (6).png',
                    'surv_shot_reload (7).png', 'surv_shot_reload (8).png', 'surv_shot_reload (9).png', 'surv_shot_reload (10).png', 'surv_shot_reload (11).png', 'surv_shot_reload (12).png',
                    'surv_shot_reload (13).png', 'surv_shot_reload (14).png', 'surv_shot_reload (15).png', 'surv_shot_reload (16).png', 'surv_shot_reload (17).png', 'surv_shot_reload (18).png',
                    'surv_shot_reload (19).png', 'surv_shot_reload (20).png']
PLAYER_RIFLE_IDLE_IMG = ['surv_rifle_idle (1).png', 'surv_rifle_idle (2).png', 'surv_rifle_idle (3).png', 'surv_rifle_idle (4).png', 'surv_rifle_idle (5).png', 'surv_rifle_idle (6).png',
                    'surv_rifle_idle (7).png', 'surv_rifle_idle (8).png', 'surv_rifle_idle (9).png', 'surv_rifle_idle (10).png', 'surv_rifle_idle (11).png', 'surv_rifle_idle (12).png',
                    'surv_rifle_idle (13).png', 'surv_rifle_idle (14).png', 'surv_rifle_idle (15).png', 'surv_rifle_idle (16).png', 'surv_rifle_idle (17).png', 'surv_rifle_idle (18).png',
                    'surv_rifle_idle (19).png', 'surv_rifle_idle (20).png',]
PLAYER_RIFLE_MOVE_IMG = ['surv_rifle_move (1).png', 'surv_rifle_move (2).png', 'surv_rifle_move (3).png', 'surv_rifle_move (4).png', 'surv_rifle_move (5).png', 'surv_rifle_move (6).png',
                    'surv_rifle_move (7).png', 'surv_rifle_move (8).png', 'surv_rifle_move (9).png', 'surv_rifle_move (10).png', 'surv_rifle_move (11).png', 'surv_rifle_move (12).png',
                    'surv_rifle_move (13).png', 'surv_rifle_move (14).png', 'surv_rifle_move (15).png', 'surv_rifle_move (16).png', 'surv_rifle_move (17).png', 'surv_rifle_move (18).png',
                    'surv_rifle_move (19).png', 'surv_rifle_move (20).png',]
PLAYER_RIFLE_SHOOT_IMG = ['surv_rifle_shoot (1).png', 'surv_rifle_shoot (2).png', 'surv_rifle_shoot (3).png']
PLAYER_RIFLE_RELOAD_IMG = ['surv_rifle_reload (1).png', 'surv_rifle_reload (2).png', 'surv_rifle_reload (3).png', 'surv_rifle_reload (4).png', 'surv_rifle_reload (5).png', 'surv_rifle_reload (6).png',
                    'surv_rifle_reload (7).png', 'surv_rifle_reload (8).png', 'surv_rifle_reload (9).png', 'surv_rifle_reload (10).png', 'surv_rifle_reload (11).png', 'surv_rifle_reload (12).png',
                    'surv_rifle_reload (13).png', 'surv_rifle_reload (14).png', 'surv_rifle_reload (15).png', 'surv_rifle_reload (16).png', 'surv_rifle_reload (17).png', 'surv_rifle_reload (18).png',
                    'surv_rifle_reload (19).png', 'surv_rifle_reload (20).png',]
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 14)

# Weapon settings
BULLET_IMG = 'bullet_pistol1.png'
BULLET_SHOTGUN_IMG = 'bullet_shotgun.png'
BULLET_RIFLE_IMG = 'bullet_rifle1.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 750,
                     'bullet_lifetime': 1300,
                     'rate': 450,
                     'kickback': 200,
                     'spread': 2,
                     'damage': 10,
                     'bullet_size': 'md',
                     'bullet_count': 1,
                     'ammo': 15,
                     'totalammo': 90,
                     'load': 15,
                     'rel_time': 3000}
WEAPONS['shotgun'] = {'bullet_speed': 700,
                      'bullet_lifetime': 1000,
                      'rate': 1000,
                      'kickback': 400,
                      'spread': 12,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'ammo': 7,
                      'totalammo': 21,
                      'load': 1,
                      'rel_time': 700}
WEAPONS['rifle'] = {'bullet_speed': 700,
                    'bullet_lifetime': 1000,
                    'rate': 100,
                    'kickback': 400,
                    'spread': 4,
                    'damage': 13,
                    'bullet_size': 'lg',
                    'bullet_count': 1,
                    'ammo': 30,
                    'totalammo': 150,
                    'load': 30,
                    'rel_time': 2000}

# Mob settings
MOB_IDLE_IMG = ['zomb_idle (1).png', 'zomb_idle (2).png', 'zomb_idle (3).png', 'zomb_idle (4).png', 'zomb_idle (5).png', 'zomb_idle (6).png',
                'zomb_idle (7).png', 'zomb_idle (8).png', 'zomb_idle (9).png', 'zomb_idle (10).png', 'zomb_idle (11).png', 'zomb_idle (12).png',
                'zomb_idle (13).png', 'zomb_idle (14).png', 'zomb_idle (15).png', 'zomb_idle (16).png', 'zomb_idle (17).png',]
MOB_MOVE_IMG = ['zomb_move (1).png', 'zomb_move (2).png', 'zomb_move (3).png', 'zomb_move (4).png', 'zomb_move (5).png', 'zomb_move (6).png',
                'zomb_move (7).png', 'zomb_move (8).png', 'zomb_move (9).png', 'zomb_move (10).png', 'zomb_move (11).png', 'zomb_move (12).png',
                'zomb_move (13).png', 'zomb_move (14).png', 'zomb_move (15).png', 'zomb_move (16).png', 'zomb_move (17).png',]
MOB_ATTACK_IMG = ['zomb_attack (1).png', 'zomb_attack (2).png', 'zomb_attack (3).png', 'zomb_attack (4).png', 'zomb_attack (5).png', 'zomb_attack (6).png',
                'zomb_attack (7).png', 'zomb_attack (8).png', 'zomb_attack (9).png']
MOB_SPEEDS = [200, 180, 160, 140, 120]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 40

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATION = 40
BLOOD_SPLASHES_RED = ['bloodsplats_0003.png', 'bloodsplats_0004.png', 'bloodsplats_0006.png']
BLOOD_SPLASHES_GREEN = ['bloodZ_0003.png', 'bloodZ_0004.png', 'bloodZ_0006.png']
BLOOD_DURATION = 20000
LIGHT_IMG = 'light2.png'
WORLD_LIGHT_IMG = 'light.png'
LIGHT_RADIUS = (600, 600)
NIGHT_COLOR = (20, 20, 20)
CROSSHAIR_PISTOL = 'crosshair012.png'
CROSSHAIR_SHOTGUN = 'crosshair020.png'
CROSSHAIR_RIFLE = 'crosshair111.png'
CROSSHAIR_OFFSET = vec(0, 14)

# Layers
WALL_LAYER = 1
BLOOD_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4

# Items
ITEM_IMAGES = {'Health': 'health_pack.png',
               'AmmoPistol': 'ammo_pistol.png',
               'AmmoShotgun': 'ammo_shotgun.png',
               'AmmoRifle': 'ammo_rifle.png',
               'Shotgun': 'shotgun.png',
               'Rifle': 'ak-47.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.3

# Objects
OBJECT_IMAGES = {'Car1': 'car_black_1.png',
                 'Car2': 'car_blue_2.png',
                 'Car3': 'car_red_3.png',
                 'Car4': 'car_yellow_4.png',
                 'Car5': 'car_green_5.png',
                 'Light': 'light.png'
                }

# Sounds
#'Kim.WeLeft.ogg'
BG_MUSIC = ['City.ogg', 'Myst.ogg', 'Road.ogg', 'Travel_0.ogg', 'Vault_0.ogg']
MENU_MUSIC = ['Setelment.ogg']
END_MUSIC = 'Alert_0.ogg'
RADIO = 'radio.ogg'
PLAYER_HIT_SOUNDS = ['pain1.wav', 'pain2.wav', 'pain3.wav', 'pain4.wav']
ZOMBIE_MOAN_SOUNDS = ['zombie_moan1.wav', 'zombie_moan2.wav', 'zombie_moan3.wav', 'zombie_moan4.wav']
ZOMBIE_HIT_SOUNDS = ['zombie_hit1.wav', 'zombie_hit2.wav', 'zombie_hit3.wav', 'zombie_hit4.wav', 'zombie_hit5.wav']
WEAPON_RELOADING_SOUNDS = {'pistol': ['pistol_reload.wav'],
                           'shotgun': ['shotgun_shell_load.wav'],
                           'rifle': ['rifle_reload.wav']}
WEAPON_FULL_SOUNDS = {'pistol': ['pistol_full.wav'],
                      'shotgun': ['shotgun_reload.wav'],
                      'rifle': ['rifle_full.wav']}
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'rifle': ['cg1.wav']}
WEAPON_EMPTY = 'weapon_empty.wav'
EFFECT_SOUNDS = {'health_up': 'health_pick.wav'}
                 #'shotgun_pickup': 'something.wav'
