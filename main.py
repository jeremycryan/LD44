import pygame
import sys
import time
import math

from frame import *
from constants import *
from projectile import *

# TODO
#
# Game end condition
# Fix fireball sprite/animation
#
# Enemy types?
#

class Game(object):

    def __init__(self):

        pygame.mixer.init(44200, -16, 2, 1024)
        pygame.mixer.pre_init()
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

        self.music_playing = True
        self.mus = pygame.mixer.Sound("LD44.wav")
        self.revive_sound = pygame.mixer.Sound("revive.wav")
        self.revive_sound.set_volume(0.45)
        self.enemy_death_sound = pygame.mixer.Sound("enemy_death.wav")
        self.enemy_death_sound.set_volume(0.16)
        self.hit_enemy_sound = pygame.mixer.Sound("hit_enemy.wav")
        self.hit_enemy_sound.set_volume(0.6)
        self.take_damage_sound = pygame.mixer.Sound("take_damage.wav")
        self.take_damage_sound.set_volume(0.6)
        self.buy_upgrade_sound = pygame.mixer.Sound("buy_upgrade.wav")
        self.player_move_sound = pygame.mixer.Sound("player_move.wav")
        self.player_move_sound.set_volume(0.07)
        self.shoot_sound = pygame.mixer.Sound("shoot.wav")
        self.shoot_sound.set_volume(0.13)
        self.email_sound = pygame.mixer.Sound("email.wav")
        self.email_sound.set_volume(0.4)
        self.work_sound = pygame.mixer.Sound("work.wav")
        self.work_sound.set_volume(0.1)

        self.game_start_sound = pygame.mixer.Sound("game_start.wav")
        self.game_start_sound.set_volume(0.7)

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

        self.messages = [self.messages[-1]]

        self.image_dict = {}
        


if __name__=="__main__":
    a = Game();
