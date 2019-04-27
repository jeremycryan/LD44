import pygame
from sprite_tools import *
from constants import *

class Enemy(object):

    def __init__(self, game):

        self.row = 3
        idle = SpriteSheet("goblin.png", (2, 1), 2)
        hurt = SpriteSheet("goblin_hurt.png", (1, 1), 1)
        self.sprite = Sprite(4)
        self.sprite.add_animation({"Idle": idle,
                                    "Hurt": hurt})
        self.sprite.start_animation("Idle")
        
        self.game = game

        self.pos = 0, 0

        self.hp = 2

        self.destroy_me = 0

        self.since_last_hit = 10

        self.active_sprite = "Idle"

    def update(self, dt, events):

        self.translate(-dt * SCROLL_SPEED)
        self.sprite.update(dt)


        hit_duration = 0.05
        self.since_last_hit += dt
        if self.since_last_hit > hit_duration and not self.active_sprite == "Idle":
            self.sprite.start_animation("Idle")
            self.active_sprite = "Idle"

    def translate(self, dx):

        self.pos = self.pos[0] + dx, self.pos[1] + dx/2

    def draw(self):

        self.sprite.x_pos = self.pos[0]
        self.sprite.y_pos = self.pos[1]
        self.sprite.draw(self.game.screen)

    def check_collisions(self, projectiles):

        for p in projectiles:
            if p.row != self.row: continue
            if p.destroyed: continue
            elif abs(p.pos[0] - self.pos[0]) < 10:
                self.get_hit()
                kill = False
                if self.destroy_me:
                    kill = True
                p.destroy(kill)
                return

    def get_hit(self):

        self.hp -= self.game.g.damage
        self.destroy_me = (self.hp <= 0)
        self.sprite.start_animation("Hurt")
        self.active_sprite = "Hurt"
        self.since_last_hit = 0

        if self.destroy_me:
            self.game.shake()
        

class Goblin(Enemy):

    pass

class Orc(Enemy):

    def __init__(self, game):
        
        self.row = 3
        idle = SpriteSheet("orc.png", (2, 1), 2)
        hurt = SpriteSheet("orc_hurt.png", (1, 1), 1)
        self.sprite = Sprite(4)
        self.sprite.add_animation({"Idle": idle,
                                    "Hurt": hurt})
        self.sprite.start_animation("Idle")
        self.active_sprite = "Idle"
        
        self.game = game

        self.pos = 0, 0

        self.hp = 5

        self.destroy_me = 0

        self.since_last_hit = 10
        
