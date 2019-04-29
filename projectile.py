import pygame
from sprite_tools import *
from constants import *

class Projectile(object):

    def __init__(self, game, player):

        idle = SpriteSheet("fireball.png", (1, 1), 1)
        destroy = SpriteSheet("explosion.png", (6, 1), 6)
        destroy_smol = SpriteSheet("smol_explosion.png", (6, 1), 6)
        self.sprite = Sprite(12)
        self.sprite.add_animation({"Idle":idle,
                                    "Destroy": destroy,
                                   "Hit": destroy_smol})
        self.sprite.start_animation("Idle")
        
        self.game = game
        self.player = player
        self.row = player.row
        self.speed = 250

        self.pos = player.pos

        self.destroy_me = 0
        self.destroy_counter = 1
        self.destroyed = False

    def translate(self, dx):
        x = self.pos[0] + dx
        y = self.pos[1] + dx/2
        self.pos = x, y

    def update(self, dt, events):
        self.translate(self.speed * dt)
        self.sprite.update(dt)

        if self.destroyed:
            self.destroy_counter -= dt
            if self.destroy_counter <= 0:
                self.destroy_me = 1

    def draw(self):

        self.sprite.x_pos, self.sprite.y_pos = self.pos
        self.sprite.draw(self.game.screen)
        
    def destroy(self, kill = False):

        if self.destroyed == False:
            self.sprite.start_animation("Hit")
            self.speed = -SCROLL_SPEED

            self.destroy_counter = 5.0/12
            self.destroyed = True

        if kill:
            self.sprite.start_animation("Destroy")
        

class Fireball(Projectile):

    def __init__(self, game, player):

        Projectile.__init__(self, game, player)
        self.speed = FIREBALL_SPEED
        self.pos = self.pos[0], self.pos[1] + TILE_HEIGHT/3
        self.game.g.shoot_sound.play()

    def destroy(self, kill = False):

        Projectile.destroy(self, kill = kill)
        if kill:
            self.pos = self.pos[0], self.pos[1] - TILE_HEIGHT/3

    
    
