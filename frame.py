import pygame

from constants import *
from enemy import *
from projectile import *
from player import *
from tile import *
import time
import sys
from menu import *

class Frame(object):

    def __init__(self, game):

        self.game = game

    def run(self):

        while True:
            dt = 0.1
            events = pygame.event.get()
            self.game.global_update(dt, events)

class FishLogo(Frame):

    def __init__(self, game):

        self.game = game
        self.logo = pygame.image.load("star_fish.png")
        self.screen = game.screen

    def run(self):

        black = pygame.Surface(GAME_SIZE)
        black.set_alpha(255)

        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.25
            events = self.game.global_update(1)
            if (time.time() - start > duration): break
        
        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.75
            
            events = self.game.global_update(1)
            
            elapsed = time.time() - start
            
            if (1 - elapsed/duration < 0): break
            
            black.set_alpha(255 * (1 - elapsed/duration))
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.logo, (GAME_WIDTH/2 - self.logo.get_width()/2,
                                        GAME_HEIGHT/2 - self.logo.get_height()/2))
            self.screen.blit(black, (0, 0))
            self.game.update_screen()

        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.75
            events = self.game.global_update(1)
            if (time.time() - start > duration): break

        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.75
            
            events = self.game.global_update(1)
            
            elapsed = time.time() - start
            
            if (1 - elapsed/duration < 0): break
            
            black.set_alpha(255 * (elapsed/duration))
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.logo, (GAME_WIDTH/2 - self.logo.get_width()/2,
                                        GAME_HEIGHT/2 - self.logo.get_height()/2))
            self.screen.blit(black, (0, 0))
            self.game.update_screen()

        return Title(self.game)

class Title(Frame):

    def __init__(self, game):

        self.game = game
        self.logo = pygame.image.load("splash.png")
        self.screen = game.screen

    def run(self):

        black = pygame.Surface(GAME_SIZE)
        black.set_alpha(255)

        enter = pygame.image.load("enter_to_begin.png")

        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.25
            events = self.game.global_update(1)
            if (time.time() - start > duration): break
        
        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.75
            
            events = self.game.global_update(1)
            
            elapsed = time.time() - start
            
            if (1 - elapsed/duration < 0): break
            
            black.set_alpha(255 * (1 - elapsed/duration))
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.logo, (GAME_WIDTH/2 - self.logo.get_width()/2,
                                        GAME_HEIGHT/2 - self.logo.get_height()/2))
            self.screen.blit(black, (0, 0))
            self.game.update_screen()

        start = time.time()
        time.sleep(0.01)
        
        while True:

            self.game.clear_screen()
            self.game.screen.blit(self.logo, (0, 0))

            if time.time() % 1 <= 0.5:
                self.game.screen.blit(enter, (234, 188))

            self.game.update_screen()

            events = self.game.global_update(0.01)
            do_break = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        do_break = True

            if do_break: break

        start = time.time()
        time.sleep(0.01)
        
        while True:

            duration = 0.75
            
            events = self.game.global_update(1)
            
            elapsed = time.time() - start
            
            if (1 - elapsed/duration < 0): break
            
            black.set_alpha(255 * (elapsed/duration))
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.logo, (GAME_WIDTH/2 - self.logo.get_width()/2,
                                        GAME_HEIGHT/2 - self.logo.get_height()/2))
            self.screen.blit(black, (0, 0))
            self.game.update_screen()

        return Level1(self.game)

class Work(Frame):

    def run(self):

        idle = SpriteSheet("cubicle.png", (2, 1), 2)
        you_sprite = Sprite(5)
        you_sprite.add_animation({"Idle": idle})
        you_sprite.start_animation("Idle")
        you_sprite.x_pos = GAME_WIDTH/2 - 60
        you_sprite.y_pos = GAME_HEIGHT/2 - 64

        self.black = pygame.Surface(GAME_SIZE)
        self.black.fill((0, 0, 0))
        self.black.set_alpha(254)
        black_alpha = 254
        black_down = True

        instruction = pygame.image.load("press_to_work.png")
        
        paused = True
        since_type = 10

        then = time.time()
        time.sleep(0.01)

        message = None

        

        while True:

            now = time.time()
            dt = now - then
            then = now

            if black_down:
                black_alpha = max(0, black_alpha - 500 * dt)
                self.black.set_alpha(black_alpha)
            else:
                black_alpha = min(255, black_alpha + 500 * dt)
                self.black.set_alpha(black_alpha)

            if black_alpha == 255:
                return Level1(self.game)

            since_type += dt
            events = self.game.global_update(dt)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    paused = False
                    since_type = 0

                    if event.key == pygame.K_ESCAPE:
                        black_down = False
            

            if since_type >= 0.25:
                paused = True
            elif black_alpha == 0:
                self.game.g.money += dt*self.game.g.income
                self.game.g.total_money += dt * self.game.g.income
            
            self.game.clear_screen()
            self.game.screen.fill((100, 100, 100))

            self.game.screen.blit(instruction, (GAME_WIDTH/2 - instruction.get_width()/2, 175))

            if not paused:
                you_sprite.update(dt)
            you_sprite.draw(self.game.screen)

            if self.game.g.total_money >= 2.9:
                self.game.g.total_money -= 2.9
                if len(self.game.g.messages):
                    message = self.game.g.messages.pop(0)

            if self.game.g.total_money >= 0.80:
                message = None

            xoff = GAME_WIDTH/2
            yoff = 189

            surfs = [self.game.g.money_font_dict[char] for char in self.format_money()]
            xoff = GAME_WIDTH/2 - sum([surf.get_width() for surf in surfs])/2 
            for surf in surfs:
                
                self.game.screen.blit(surf, (xoff, yoff))
                xoff += surf.get_width()

            if message:
                self.game.screen.blit(message, (148, 24))

            self.game.screen.blit(self.black, (0, 0))

            self.game.update_screen()

    def format_money(self):

        a = "$" + str(round(self.game.g.money, 2))
        while len(a.split(".")[1]) < 2:
            a += "0"

        return a
            

class Level1(Frame):

    def run(self):


        self.lose_menu = LoseMenu(self.game)

        self.since_last_fireball = 0
        self.space_pressed = 0
        self.player = Player(self.game)
        
        rows = []
        pillars = []
        back_tiles = []
        clouds = []

        self.black = pygame.Surface(GAME_SIZE)
        self.black.fill((0, 0, 0))
        self.black.set_alpha(254)
        black_alpha = 254
        black_down = True

        self.fortress_bar = pygame.image.load("fortress_bar.png")
        self.load_bar = pygame.Surface((72, 6))
        self.load_bar.fill((70, 120, 255))
        self.load_bar_highlight = pygame.Surface((72, 3))
        self.load_bar_highlight.fill((45, 90, 240))
        self.game.g.fortress_health = self.game.g.fortress_max_health
        self.disp_hp = 1

        clouds.append(Cloud(self.game, start = True))

        self.game.g.stars = 0

        bk_width = 316
        for x in [0, bk_width, bk_width * 2]:
            for y in [0, bk_width, bk_width * 2]:
                
                back_tiles.append(Backdrop(self.game, x, y))


        first_row = Row(self.game)
        first_row.translate(-TILE_WIDTH * 11, -TILE_HEIGHT * 11)
        rows.append(first_row)
        
        then = time.time()
        even = True
        time.sleep(0.01)
        num_rows = 0

        self.projectiles = []
        self.enemies = []

        self.killed = 0

        since_cloud = 0
        spend = 0
        spend_incr = self.game.g.damage / self.game.g.projectile_period / 2.5
        
        while True:

            if self.game.g.gameover:
                self.lose_menu.killed(self.killed)
                self.lose_menu.show()
                self.game.g.fortress_health = 0
            else:
                self.game.g.stars = 0

            now = time.time()
            dt = now - then
            then = now

            if dt <= 0: dt = 0.01

            spend += spend_incr * dt
            spend_incr *= 1.02**dt

            if black_down:
                black_alpha = max(0, black_alpha - 500 * dt)
                self.black.set_alpha(black_alpha)
            else:
                black_alpha = min(255, black_alpha + 500 * dt)
                self.black.set_alpha(black_alpha)

            events = self.game.global_update(dt)
            next_frame = self.check_events(dt, events)

            if next_frame != 0:
                break

            self.game.clear_screen()

            last = rows[-1]
            while last.pos()[0] < GAME_WIDTH + TILE_WIDTH*2:
                even = 1 - even
                num_rows += 1
                rows.append(Row(self.game,
                                even,
                                x = last.pos()[0] + TILE_WIDTH//2,
                                y = last.pos()[1] + TILE_HEIGHT//2))
                last = rows[-1]

                if num_rows % 2 == 0 and num_rows > 30:
                    available_rows = [1, 2, 3, 4, 5]
                    random.shuffle(available_rows)
                    while spend > 0 and len(available_rows):

                        e = random.choice(["goblin", "orc"])
                        if num_rows < 100:
                            e = "goblin"
                        self.make_enemy(available_rows.pop(), rows, e)
                        if e == "orc": spend -= 5
                        else: spend -= 2
                    
                if num_rows % 3 == 1:
                    pillars.append(Pillar(self.game, last.pos()[0] - 3 * TILE_WIDTH,
                                          last.pos()[1] + 3*TILE_HEIGHT))
                

            back_tiles.sort(key=lambda a: a.pos[0])
            while back_tiles[0].pos[0] < -bk_width:
                back_tiles[0].translate(bk_width * 3, 0, parallax = False)
                back_tiles.sort(key=lambda a: a.pos[0])

            back_tiles.sort(key=lambda a: a.pos[1])
            while back_tiles[0].pos[1] < -bk_width:
                back_tiles[0].translate(0, bk_width * 3, parallax = False)
                back_tiles.sort(key=lambda a: a.pos[1])

            for b in back_tiles:
                b.update(dt, events)
                b.draw()

            clouds.sort(key = lambda a: a.pos[0])
            while clouds[0].pos[0] < -100:
                clouds = clouds[1:]

            since_cloud += dt
            if since_cloud > 3:
                clouds.append(Cloud(self.game))
                since_cloud = 0

            for c in clouds:
                c.update(dt, events)
                c.draw()

            if rows[0].pos()[0] < -TILE_WIDTH:
                rows = rows[1:]

            for a in rows:
                a.update(dt, events)
                a.draw()

            if len(self.enemies):
                while self.enemies[0].pos[0] < -TILE_WIDTH:
                    popped = self.enemies.pop(0)
                    self.damage_fortress(popped.hp)
                    if not len(self.enemies): break

            i = 0
            while i < len(self.enemies):
                e = self.enemies[i]
                if e.destroy_me:
                    self.enemies.pop(i)
                    self.killed += 1
                    continue
                e.check_collisions(self.projectiles)
                e.update(dt, events)
                e.draw()
                i += 1

            if pillars[0].pos[0] < -TILE_WIDTH*4:
                pillars = pillars[1:]

            for p in pillars:
                p.update(dt, events)
                p.draw()

            self.player.update(dt, events)
            self.player.draw()

            if len(self.projectiles):
                while self.projectiles[0].pos[0] > GAME_WIDTH:
                    self.projectiles.pop(0)
                    if not len(self.projectiles): break
                    
            for i, p in enumerate(self.projectiles):
                if p.destroy_me:
                    self.projectiles.pop(i)
                    continue
                p.update(dt, events)
                p.draw()

            print(len(self.projectiles))

            self.draw_fortress_bar(dt)

            next_frame = self.lose_menu.update(dt, events)
            if next_frame:
                break
            
            self.lose_menu.draw()

            self.game.screen.blit(self.black, (0, 0))
            self.game.update_screen()

        then = time.time()
        time.sleep(0.01)
        self.lose_menu.draw()
        
        while black_alpha < 10:
            now = time.time()
            dt = now - then
            then = now

            events = self.game.global_update(dt)

            black_alpha = min(100, black_alpha + 24 * dt)
            self.black.set_alpha(black_alpha)

            self.lose_menu.update(dt, events)

            self.game.screen.blit(self.black, (0, 0))
            self.game.update_screen()

        if next_frame == 1:
            return Level1(self.game)
        else:
            return next_frame(self.game)

    def damage_fortress(self, amt):

        self.game.g.fortress_health = max(0, self.game.g.fortress_health - amt)
        if self.game.g.fortress_health <= 0.1:
            self.lose_menu.killed(self.killed)
            self.lose_menu.show()
        else:
            self.game.shake(15)

    def draw_fortress_bar(self, dt):

        self.game.screen.blit(self.fortress_bar, (290, 20))
        hp = self.game.g.fortress_health/self.game.g.fortress_max_health
        dhp = hp - self.disp_hp
        self.disp_hp += dt * dhp * 5
        bar = pygame.transform.scale(self.load_bar, (int(72 * self.disp_hp), 6))
        self.game.screen.blit(bar, (290 + 31, 20 + 14))
        bar2 = pygame.transform.scale(self.load_bar_highlight, (bar.get_width(), 3))
        self.game.screen.blit(bar2, (290 + 31, 20 + 14))
        pass

    def check_events(self, dt, events):

        self.since_last_fireball += dt

        fireball_period = self.game.g.projectile_period
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.lose_menu.hidden:
                    if event.key == pygame.K_SPACE:
                        self.space_pressed = 1
                if event.key == pygame.K_ESCAPE:
                    self.game.g.gameover = True
                    return Work
                if event.key == pygame.K_r:
                    self.lose_menu.show()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_pressed = 0


        if self.space_pressed and self.since_last_fireball > fireball_period:
            
            self.since_last_fireball -= fireball_period           
            self.projectiles.append(self.game.g.projectile(self.game, self.player))

        elif not self.space_pressed and self.since_last_fireball > fireball_period:

            self.since_last_fireball = fireball_period

        return 0

                    
    def make_enemy(self, row, rows, enemy = "goblin", random_row = False):

        if enemy == "goblin":
            new_enemy = Goblin(self.game)

        elif enemy == "orc":
            new_enemy = Orc(self.game)

        else:
            new_enemy = Goblin(self.game)

        if random_row:
            new_enemy.row = random.choice([0, 1, 2, 3, 4])
        else:
            new_enemy.row = row
            
        new_enemy.pos = rows[-1].tiles[row].pos
        self.enemies.append(new_enemy)

        













            
    
