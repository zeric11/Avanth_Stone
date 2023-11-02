import pygame
from maps import *
from player import Player
from tile import Tile


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()

    def create_map(self):
        for i in range(len(MAP_0)):
            for j in range(len(MAP_0[0])):
                item = MAP_0[i][j]
                if item == "p":
                    self.player = Player((j * TILE_SIZE, i * TILE_SIZE), [self.visible_sprites], self.obstacle_sprites)
                elif item == "x":
                    Tile((j * TILE_SIZE, i * TILE_SIZE), [self.visible_sprites, self.obstacle_sprites])
