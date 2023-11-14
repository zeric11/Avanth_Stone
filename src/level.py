import pygame
from maps import *
from player import Player
from enemy import Enemy
from tile import Tile


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)


    def create_map(self):
        for i in range(len(MAP_0)):
            for j in range(len(MAP_0[0])):
                item = MAP_0[i][j]
                if item == "p":
                    self.player = Player((j * TILE_SIZE, i * TILE_SIZE), 
                                         [self.visible_sprites], 
                                         self.obstacle_sprites)
                elif item == "g":
                    Enemy("ghost", 
                          (j * TILE_SIZE, i * TILE_SIZE), 
                          [self.visible_sprites, self.attackable_sprites], 
                          self.obstacle_sprites)
                elif item == "x":
                    Tile((j * TILE_SIZE, i * TILE_SIZE), 
                         [self.visible_sprites, self.obstacle_sprites], 
                         "rock")


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
