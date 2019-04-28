import pygame
from constants import *
import random

class Tile(object):

    def __init__(self, game):

        self.game = game
        path = "tile1.png"
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)
        self.pos = (GAME_WIDTH, GAME_HEIGHT)

    def translate(self, dx, dy):

        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def scroll(self, dt):

        dx = -SCROLL_SPEED*dt
        dy = -SCROLL_SPEED/2*dt
        self.translate(dx, dy)

        return(dx, dy)

    def draw(self):

        x, y = self.pos
        if x%4 < 2 == 0 and y%2 >= 1:
            y -= 1
        
        self.game.screen.blit(self.sprite, (x, y))

    def update(self, dt, events):

        dx, dy = self.scroll(dt)
        return dx, dy

class LightTile(Tile):

    def __init__(self, game):

        self.game = game

        self.pos = (GAME_WIDTH/2, GAME_HEIGHT/2)
        path = "tile1.png"
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)

class DarkTile(Tile):

    def __init__(self, game):

        self.game = game
        path = "tile2.png"
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)
        self.pos = (GAME_WIDTH/2, GAME_HEIGHT/2)

class Edging(Tile):

    def __init__(self, game):

        self.game = game
        path = "edging.png"
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)
        self.pos = (GAME_WIDTH/2, GAME_HEIGHT/2)

class Row(object):

    def __init__(self, game, even = True, x = GAME_WIDTH, y = GAME_HEIGHT*0.65):

        self.game = game
        self.tiles = []

        x, y = x, y

        for i in range(7):

            if i in [0, 6]: new_tile = Edging(game)
            elif even: new_tile = LightTile(game)
            else: new_tile = DarkTile(game)

            new_tile.pos = (x, y)
            self.tiles.append(new_tile)

            x -= TILE_WIDTH//2
            y += TILE_HEIGHT//2
                        
            even = 1 - even
        

    def update(self, dt, events):

        for tile in self.tiles: tile.update(dt, events)

    def draw(self):

        for tile in self.tiles: tile.draw()

    def pos(self):

        return self.tiles[0].pos

    def translate(self, dx, dy):

        for item in self.tiles:
            item.translate(dx, dy)

class Pillar(Tile):

    def __init__(self, game, x = 0, y = 0):

        self.game = game
        path = "pillars.png"
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)
        self.pos = (x, y)

class Backdrop(Tile):

    def __init__(self, game, x = 0, y = 0):

        self.game = game
        path = "background.png"
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)
        self.pos = (x, y)

    def translate(self, dx, dy, parallax = True):

        parallax_factor = 0.2
        if not parallax:
            parallax_factor = 1
        self.pos = (self.pos[0] + dx*parallax_factor, self.pos[1] + dy * parallax_factor)

class Cloud(Tile):


    def __init__(self, game, start = False):

        self.game = game
        sprites = ["cloud_1.png", "cloud_2.png"]
        self.parallax_factor = random.choice([0.4])
        path = random.choice(sprites)
        if path in self.game.g.image_dict:
            self.sprite = self.game.g.image_dict[path].copy()
        else:
            self.sprite = pygame.image.load(path)

        self.pos = (GAME_WIDTH, GAME_HEIGHT * 0.8)
        if start:
            self.pos = (random.random() * GAME_WIDTH,
                        random.random() * GAME_HEIGHT)
        self.translate(0, - random.random() * GAME_HEIGHT * 0.7, parallax = False)


    def translate(self, dx, dy, parallax = True):

        parallax_factor = self.parallax_factor
        if not parallax:
            parallax_factor = 1
        self.pos = (self.pos[0] + dx*parallax_factor, self.pos[1] + dy * parallax_factor)

        
    
