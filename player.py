from sprite_tools import *
from constants import *
import pygame

class Player(object):

    def __init__(self, game):
        
        self.game = game

        self.row = 3

        idle = SpriteSheet("wizurr.png", (4, 1), 4)

        self.sprite = Sprite(10)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.start_animation("Idle")

        self.pos = GAME_WIDTH/3, GAME_HEIGHT/3
        self.render_pos = self.pos

    def draw(self):

        self.sprite.x_pos = self.render_pos[0]
        self.sprite.y_pos = self.render_pos[1]
        self.sprite.draw(self.game.screen)

    def update(self, dt, events):

        self.sprite.update(dt)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.move_right()

        dx = self.pos[0] - self.render_pos[0]
        dy = self.pos[1] - self.render_pos[1]

        if (abs(dx) + abs(dy) >= 2):
            self.render_pos = (self.render_pos[0] + dx * dt * 25,
                        self.render_pos[1] + dy * dt * 25)

    def translate(self, dx, dy):
        self.pos = self.pos[0] + dx, self.pos[1] + dy

    def move_left(self):

        if self.row < 5:
            self.row += 1
            self.translate(-TILE_WIDTH//2, TILE_HEIGHT//2)

    def move_right(self):

        if self.row > 1:
            self.row -= 1
            self.translate(TILE_WIDTH//2, -TILE_HEIGHT//2)
