from constants import *
import pygame

class LoseMenu(object):

    def __init__(self, game):

        self.game = game
        self.sprite = pygame.image.load("losing_screen.png")
        self.black = pygame.Surface(GAME_SIZE)
        self.black.fill((0, 0, 0))
        self.black_alpha = 0
        self.yoff = 80
        self.y = GAME_HEIGHT + self.yoff
        self.target_y = self.y
        self.hidden = True

        self.buttons = [SpeedBoost(self.game, self),
                        PowerBoost(self.game, self),
                        Revive(self.game, self)]

        self.star = pygame.image.load("star.png")
        self.half_star = pygame.image.load("half_star.png")

        self.return_level = False

        self.kill_ct = 0

    def killed(self, num):
        self.kill_ct = num

    def update(self, dt, events):

        if self.hidden:
            self.black_alpha = max(0, self.black_alpha - dt*400)
            self.yoff = min(80, self.yoff + 150*dt)
        else:
            self.black_alpha = min(150, self.black_alpha + dt*400)
            self.yoff = max(0, self.yoff - 150*dt)
        self.black.set_alpha(self.black_alpha)
        self.y += (self.target_y - self.y) * dt * 8

        for button in self.buttons:
            button.update(dt, events)

        if self.return_level:
            return self.return_level

    def draw(self):


        self.game.screen.blit(self.black, (0, 0))
        if self.y <= GAME_HEIGHT:
            self.game.screen.blit(self.sprite, (0, self.y - self.yoff))

            surfs = [self.game.g.money_font_dict[char] for char in self.format_money()]

            x = 339 - sum([surf.get_width() for surf in surfs])/2
            y = self.y - self.yoff + 80
            for surf in surfs:
                self.game.screen.blit(surf, (x, y))
                x += surf.get_width()

            for button in self.buttons:
                button.draw()

        stars = 0

        if self.kill_ct > 0: stars += 0.5
        if self.kill_ct > 15: stars += 0.5
        if self.kill_ct > 30: stars += 0.5
        if self.kill_ct > 60: stars += 0.5
        if self.kill_ct > 100: stars += 0.5
        if self.kill_ct > 150: stars += 0.5

        self.game.g.stars = stars

        pos_1 = (140, 98 + self.y - self.yoff)
        pos_2 = (185, 94 + self.y - self.yoff)
        pos_3 = (231, 98 + self.y - self.yoff)

        if stars >= 3:
            self.game.screen.blit(self.star, pos_3)
        elif stars >= 2.5:
            self.game.screen.blit(self.half_star, pos_3)

        if stars >= 2:
            self.game.screen.blit(self.star, pos_2)
        elif stars >= 1.5:
            self.game.screen.blit(self.half_star, pos_2)

        if stars >= 1:
            self.game.screen.blit(self.star, pos_1)
        elif stars >= 0.5:
            self.game.screen.blit(self.half_star, pos_1)


    def format_money(self):

        a = "$" + str(round(self.game.g.money, 2))
        while len(a.split(".")[1]) < 2:
            a += "0"

        return a

    def show(self):

        self.target_y = 0
        self.hidden = False
        self.game.g.gameover = True
        self.game.g.mus.set_volume(0.3)

    def hide(self):

        self.target_y = GAME_HEIGHT
        self.hidden = True
        self.game.g.mus.set_volume(1)

class Button(object):

    def __init__(self, game, parent):

        self.game = game
        self.parent = parent

        self.cost = 5.99

        self.default_surf = pygame.image.load("speed_boost_default.png")
        self.hover_surf = pygame.image.load("speed_boost_hover.png")
        self.disabled_surf = pygame.image.load("speed_boost_disabled.png")

        self.pos = (41, 165)

        self.state = "Default"

    def update(self, dt, events):

        mpos = pygame.mouse.get_pos()
        if self.game.g.money < self.cost:
            self.state = "Disabled"
        elif self.pos_in_rect(mpos):
            self.state = "Hover"
        else:
            self.state = "Default"

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.state == "Hover":
                    self.click()

    def click(self):
        pass

    def draw(self):

        x = self.pos[0]
        y = self.parent.y - self.parent.yoff + self.pos[1]
        pos = (x, y)        

        if self.state == "Default":
            self.game.screen.blit(self.default_surf, pos)
        elif self.state == "Hover":
            self.game.screen.blit(self.hover_surf, pos)
        elif self.state == "Disabled":
            self.game.screen.blit(self.disabled_surf, pos)

    def pos_in_rect(self, pos):

        scale = WINDOW_WIDTH/GAME_WIDTH

        min_x = self.pos[0]
        max_x = self.pos[0] + self.default_surf.get_width()
        min_y = self.pos[1] + self.parent.y - self.parent.yoff
        max_y = self.pos[1] + self.default_surf.get_height() + self.parent.y - self.parent.yoff

        if pos[0] < min_x * scale: return False
        if pos[0] > max_x * scale: return False
        if pos[1] < min_y * scale: return False
        if pos[1] > max_y * scale: return False
        return True

class SpeedBoost(Button):

    def click(self):
        self.game.g.projectile_period *= 0.75
        self.game.g.money -= self.cost
        self.game.g.buy_upgrade_sound.play()

class PowerBoost(Button):

    def __init__(self, game, parent):

        self.cost = 8.99

        self.game = game
        self.parent = parent

        self.default_surf = pygame.image.load("power_boost_default.png")
        self.hover_surf = pygame.image.load("power_boost_hover.png")
        self.disabled_surf = pygame.image.load("power_boost_disabled.png")

        self.pos = (267, 163)

        self.state = "Default"

    def click(self):
        self.game.g.damage += 1
        self.game.g.money -= self.cost
        self.game.g.buy_upgrade_sound.play()

class Revive(Button):

    def __init__(self, game, parent):

        self.cost = 1.99

        self.game = game
        self.parent = parent

        self.default_surf = pygame.image.load("revive_default.png")
        self.hover_surf = pygame.image.load("revive_hover.png")
        self.disabled_surf = pygame.image.load("revive_disabled.png")

        self.pos = (158, 146)

        self.state = "Default"

    def click(self):
        
        self.game.g.gameover = False
        self.parent.hide()
        self.game.g.money -= self.cost
        self.parent.return_level = True

        self.game.g.buy_upgrade_sound.play()
    
