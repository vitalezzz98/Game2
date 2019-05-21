# Tile game by Vitalezzz98
# Top down tiles pack by Kenney.nl
# Particles pack by Kenney.nl
# Smoke Particles by Kenney.nl
# Player model by rileygombart
# Zombie model by rileygombart
# Player sounds by Michel Baradari
# Shots sounds by Michel Baradari
# Zombie sounds by artisticdude
# Inventory sounds by artisticdude
# Post apocalypse soundtrack by Alexandr Zhelanov, https://soundcloud.com/alexandr-zhelanov
# "And Then We Left" by Kim Lightyear

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from random import choice, random

# HUD
font_name = pg.font.match_font('arial')
def draw_texts(surf, text, size, x, y):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        #game_folder = path.dirname(__file__)
        img_folder = path.join(path.dirname(__file__), 'sprites')
        map_folder = path.join(path.dirname(__file__), 'maps')
        snd_folder = path.join(path.dirname(__file__), 'sound')
        music_folder = path.join(path.dirname(__file__), 'music')
        player_img_folder = path.join(path.dirname(__file__), 'player')
        zombie_img_folder = path.join(path.dirname(__file__), 'zombie')
        self.font = path.join(path.dirname(__file__), 'Apocalypse.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map = TiledMap(path.join(map_folder, 'tilemap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.player_idles = []
        for img in PLAYER_IDLE_IMG:
            self.player_idles.append(pg.image.load(path.join(player_img_folder, img)).convert_alpha())
        self.player_moves = []
        for img in PLAYER_MOVE_IMG:
            self.player_moves.append(pg.image.load(path.join(player_img_folder, img)).convert_alpha())
        self.player_shoots = []
        for img in PLAYER_SHOOT_IMG:
            self.player_shoots.append(pg.image.load(path.join(player_img_folder, img)).convert_alpha())
        self.mob_idles = []
        for img in MOB_IDLE_IMG:
            self.mob_idles.append(pg.image.load(path.join(zombie_img_folder, img)).convert_alpha())
        self.mob_moves = []
        for img in MOB_MOVE_IMG:
            self.mob_moves.append(pg.image.load(path.join(zombie_img_folder, img)).convert_alpha())
        self.mob_attacks = []
        for img in MOB_ATTACK_IMG:
            self.mob_attacks.append(pg.image.load(path.join(zombie_img_folder, img)).convert_alpha())
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.blood_red = []
        for img in BLOOD_SPLASHES_RED:
            self.blood_red.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.blood_green = []
        for img in BLOOD_SPLASHES_GREEN:
            self.blood_green.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, choice(BG_MUSIC)))
        pg.mixer.music.set_volume(MUSIC_VOLUME)
        self.effects_sounds = {}
        for type in EFFECT_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECT_SOUNDS[type]))
        self.weapons_sounds = {}
        self.weapons_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(SOUNDS_VOLUME)
            self.weapons_sounds['gun'].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(SOUNDS_VOLUME)
            self.zombie_moan_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(SOUNDS_VOLUME)
            self.zombie_hit_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(SOUNDS_VOLUME)
            self.player_hit_sounds.append(s)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'Player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'Zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'Wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['Health']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.mouse = Mouse(self, self.player.pos.x, self.player.pos.y)
        self.draw_debug = False
        self.draw_debug_1 = False
        self.draw_debug_2 = False
        self.draw_debug_3 = False
        self.draw_debug_4 = False
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # player hit items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'Health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
        # zombie hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            BloodSplashRed(self, self.player.pos)
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullet hits
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            if random() < 0.5:
                choice(self.zombie_hit_sounds).play()
            if hit.target_dist.length_squared() > hit.detect_radius**2:
                hit.detect_radius += 100
            BloodSplashGreen(self, hit.pos)
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
                if self.draw_debug_1:
                    self.draw_text('Mouse Screen X, Y: ' + str(pg.mouse.get_pos()), self.font, 22, WHITE, 10, 60, align='nw')
                if self.draw_debug_2:
                    self.draw_text('Mouse rel. to Player X, Y: ' + str(pg.mouse.get_pos()), self.font, 22, WHITE, 10, 90, align='nw')
                if self.draw_debug_3:
                    self.draw_text('Mouse World X, Y: ' + str(pg.mouse.get_pos()), self.font, 22, WHITE, 10, 120, align='nw')
                if self.draw_debug_4:
                    self.draw_text('Player X, Y: ' + str(pg.mouse.get_pos()), self.font, 22, WHITE, 10, 150, align='nw')
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD draw
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, 105, DARK_RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_F1:
                    self.draw_debug_1 = not self.draw_debug_1
                if event.key == pg.K_F2:
                    self.draw_debug_2 = not self.draw_debug_2
                if event.key == pg.K_F3:
                    self.draw_debug_3 = not self.draw_debug_3
                if event.key == pg.K_F4:
                    self.draw_debug_4 = not self.draw_debug_4

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
g.show_go_screen()
