import pygame as pg
from random import uniform, choice, randint, random, randrange
from settings import *
from tilemap import collide_hit_rect
import math
import pytweening as tween
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Mouse(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface([10, 10], pg.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.pos = self.game.camera.reverse(pg.mouse.get_pos())
        self.x = self.pos[0] - self.game.player.pos.x
        self.y = self.pos[1] - self.game.player.pos.y
        self.angle = math.atan2(self.x, self.y)
        self.angle = (180 / math.pi) * (-self.angle)
        self.hit_rect = self.rect

    def update(self):
        self.pos = self.game.camera.reverse(pg.mouse.get_pos())
        self.x = self.pos[0] - self.game.player.pos.x
        self.y = self.pos[1] - self.game.player.pos.y
        self.angle = math.atan2(self.x, self.y)
        self.angle = (180 / math.pi) * (-self.angle)
        self.hit_rect = self.rect

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image = pg.transform.scale(game.player_idles[self.current_frame], (64, 55))
        self.image_copy = pg.transform.rotate(self.image, 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.x = x
        self.y = y
        self.rot = 0
        self.last_shot = 0
        self.last_reload = 0
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.ammo = WEAPONS[self.weapon]['ammo']
        self.shooting = False
        self.reloading = False
        self.flashlight = False

    def get_keys(self):
        self.vel = vec(0, 0)
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel[0] =(-PLAYER_SPEED)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel[0] = (PLAYER_SPEED)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel[1] = (-PLAYER_SPEED)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel[1] = (PLAYER_SPEED)
        if self.vel[0] != 0 and self.vel[1] != 0:
            self.vel[0] *= 0.7071
            self.vel[1] *= 0.7071
        if mouse[0]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if self.ammo > 0:
            if now - self.last_shot > WEAPONS[self.weapon]['rate']:
                self.last_shot = now
                dir = vec(1, 0).rotate(self.game.mouse.angle + 90)
                pos = self.pos + BARREL_OFFSET.rotate(self.game.mouse.angle + 90)
                self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(self.game.mouse.angle + 90)
                for i in range(WEAPONS[self.weapon]['bullet_count']):
                    spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                    Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                    snd = choice(self.game.weapons_sounds[self.weapon])
                    if snd.get_num_channels() > 2:
                        snd.stop()
                    snd.play()
                self.ammo -= 1
                MuzzleFlash(self.game, pos)

    def reload(self):
        now = pg.time.get_ticks()
        if now - self.last_reload > WEAPONS[self.weapon]['rel_time']:
            self.reloading = True
            if self.ammo >= WEAPONS[self.weapon]['ammo']:
                snd = choice(self.game.weapon_full_sounds[self.weapon])
                self.reloading = False
                if snd.get_num_channels() > 1:
                    snd.stop()
                snd.play()
            else:
                snd = choice(self.game.weapons_reload_sounds[self.weapon])
                if snd.get_num_channels() > 1:
                    snd.stop()
                snd.play()
            self.last_reload = now
            self.ammo += WEAPONS[self.weapon]['load']
            if self.ammo >= WEAPONS[self.weapon]['ammo']:
                self.ammo = WEAPONS[self.weapon]['ammo']

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def update(self):
        mouse = pg.mouse.get_pressed()
        if self.vel == (0, 0) and not self.shooting and not self.reloading:
            self.standing = True
        else:
            self.standing = False
        if self.vel != (0, 0) and not self.shooting and not self.reloading:
            self.moving = True
        else:
            self.moving = False
        if mouse[0]:
            self.shooting = True
        now = pg.time.get_ticks()
        if self.weapon == 'pistol':
            if self.standing:
                if now - self.last_update > 50:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_idles)
                    self.image = pg.transform.scale(self.game.player_idles[self.current_frame], (64, 55))
                    self.image_copy = pg.transform.rotate(self.image, 270)
            if self.moving:
                if now - self.last_update > 20:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_moves)
                    self.image = pg.transform.scale(self.game.player_moves[self.current_frame], (64, 55))
                    self.image_copy = pg.transform.rotate(self.image, 270)
            if self.shooting and self.ammo > 0:
                if now - self.last_update > 150:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_shoots)
                    self.image = pg.transform.scale(self.game.player_shoots[self.current_frame], (64, 55))
                    self.image_copy = pg.transform.rotate(self.image, 270)
                    if not mouse[0] and self.current_frame == len(self.game.player_shoots) - 1:
                        self.shooting = False
            if self.reloading:
                if now - self.last_update > 150:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_reloads)
                    self.image = pg.transform.scale(self.game.player_reloads[self.current_frame], (65, 58))
                    self.image_copy = pg.transform.rotate(self.image, 270)
                    if self.current_frame == len(self.game.player_reloads) - 1:
                        self.reloading = False
        elif self.weapon == 'shotgun':
            if self.standing:
                if now - self.last_update > 50:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_shotgun_idles)
                    self.image = pg.transform.scale(self.game.player_shotgun_idles[self.current_frame], (64, 55))
                    self.image_copy = pg.transform.rotate(self.image, 270)
            if self.moving:
                if now - self.last_update > 20:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_shotgun_moves)
                    self.image = pg.transform.scale(self.game.player_shotgun_moves[self.current_frame], (64, 55))
                    self.image_copy = pg.transform.rotate(self.image, 270)
            if self.shooting and self.ammo > 0:
                if now - self.last_update > 150:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_shotgun_shoots)
                    self.image = pg.transform.scale(self.game.player_shotgun_shoots[self.current_frame], (64, 55))
                    self.image_copy = pg.transform.rotate(self.image, 270)
                    if not mouse[0] and self.current_frame == len(self.game.player_shoots) - 1:
                        self.shooting = False
            if self.reloading:
                if now - self.last_update > 25:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.game.player_shotgun_reloads)
                    self.image = pg.transform.scale(self.game.player_shotgun_reloads[self.current_frame], (65, 58))
                    self.image_copy = pg.transform.rotate(self.image, 270)
                    if self.current_frame == len(self.game.player_reloads) - 1:
                        self.reloading = False
        self.get_keys()
        self.image = pg.transform.rotate(self.image_copy, int(-self.game.mouse.angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        # self.hit_rect.centerx = self.pos.x
        # collide_with_walls(self, self.game.obstacles, 'x')
        # self.hit_rect.centery = self.pos.y
        # collide_with_walls(self, self.game.obstacles, 'y')
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect.center = self.hit_rect.center

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image = pg.transform.scale(game.mob_idles[self.current_frame], (63, 57))
        self.image_copy = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        self.target_dist = self.target.pos - self.pos
        self.detect_radius = 400

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.target_dist = self.target.pos - self.pos
        self.rot = self.target_dist.angle_to(vec(1, 0))
        now = pg.time.get_ticks()
        if self.vel == (0, 0):
            self.idle = True
        else:
            self.idle = False
        if self.vel != (0, 0):
            self.walking = True
        else:
            self.walking = False
        if self.idle:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.mob_idles)
                self.image = pg.transform.scale(self.game.mob_idles[self.current_frame], (63, 57))
                self.image_copy = self.image
                self.image = pg.transform.rotate(self.image_copy, self.rot)
                self.rect = self.image.get_rect()
                self.rect.center = self.pos
        if self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.game.mob_moves)
                self.image = pg.transform.scale(self.game.mob_moves[self.current_frame], (70, 76))
                self.image_copy = self.image
                self.rect.center = self.pos
        if self.target_dist.length_squared() < self.detect_radius**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.image = pg.transform.rotate(self.image_copy, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        else:
            self.vel = vec(0, 0)
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']], -game.mouse.angle + 270)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * (WEAPONS[game.player.weapon]['bullet_speed'] + choice([-15, 0, 15, 30]))
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(10, 20)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class BloodSplashRed(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = BLOOD_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 64
        self.image = pg.transform.scale(choice(game.blood_red), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BLOOD_DURATION:
            self.kill()

class BloodSplashGreen(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = BLOOD_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 64
        self.image = pg.transform.scale(choice(game.blood_green), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BLOOD_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Object(pg.sprite.Sprite):
    def __init__(self, game, pos, rotation, type):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.object_images[type], -rotation % 360)
        #self.image_copy = pg.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, rotation):
        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

# class SoftObstacle(pg.sprite.Sprite):
#     def __init__(self, game, x, y, w, h):
#         self.groups = game.obstacles
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.rect = pg.Rect(x, y, w, h)
#         self.x = x
#         self.y = y
#         self.rect.x = x
#         self.rect.y = y
