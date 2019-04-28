import pygame
import sys
import time
import math

from frame import *
from constants import *
from projectile import *

# TODO
#
# Music/Audio
# Game end condition
# Stars on killing enemies
# Fix fireball sprite/animation
# Tutorial/instruction
#
# Enemy types?
#

class Game(object):

    def __init__(self):

        pygame.init();
        pygame.font.init()
        self.g = Globals()

        self.screen = pygame.Surface(GAME_SIZE)
        self.screen_commit = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Microtransaction Mages")

        self.shake_offset = 0

        self.main()

    def shake(self, amp=4):

        self.shake_offset = max(amp, self.shake_offset)

    def main(self):

        next_frame = FishLogo(self)

        while True:
            next_frame = next_frame.run()


    def global_update(self, dt):

        self.shake_offset *= 0.01**dt
        if self.shake_offset <= 1:
            self.shake_offset = 0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        return events

    def update_screen(self):

        yoff = self.shake_offset * math.sin(time.time() * 50)

        new = pygame.transform.scale(self.screen, WINDOW_SIZE)
        self.screen_commit.blit(new, (0, yoff))
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

class Globals(object):

    def __init__(self):
        self.money = STARTING_MONEY
        self.income = 0.16

        self.fortress_max_health = 10
        self.fortress_health = self.fortress_max_health

        self.money_font = pygame.font.Font("monospace.ttf", 15)
        self.money_font_dict = {}

        for char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "$", ".", "-"]:
            self.money_font_dict[char] = self.money_font.render(char, 0, WHITE)

        self.damage = 1
        self.projectile = Fireball
        self.projectile_period = 0.3

        self.gameover = False

        self.total_money = 2

        self.messages = []
        for message in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            self.messages.append(pygame.image.load("message%s.png" % message))

        self.image_dict = {}
        


if __name__=="__main__":
    a = Game();
