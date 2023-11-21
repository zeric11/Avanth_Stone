import pygame
from maps import *
from player import Player
from enemy import Enemy
from ghost import Ghost
from sentry import Sentry
from orb import Orb
from bomber import Bomber
from meteor import Meteor
from tile import Tile
from csv import reader
from os import walk


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
        self.enemy_update(self.player)

    
    def create_map(self):
        layouts = {
            "Entities" : import_csv_layout("../map/map_Entities.csv"),
            "Objects" : import_csv_layout("../map/map_Objects.csv"),
            "Decor" : import_csv_layout("../map/map_Decor.csv"),
            "Shrubs" : import_csv_layout("../map/map_Shrubs.csv"),
            "Logs" : import_csv_layout("../map/map_Logs.csv"),
            "Trees" : import_csv_layout("../map/map_Trees.csv"),
            "Boss door" : import_csv_layout("../map/map_Boss door.csv"),
            "Water" : import_csv_layout("../map/map_Water.csv"),
            "Stone border" : import_csv_layout("../map/map_Stone border.csv"),
            "Border" : import_csv_layout("../map/map_Border.csv"),
            "Floor" : import_csv_layout("../map/map_Floor.csv"),
        }
        nature_textures = import_folder("../textures/nature")
        
        for layer, layout in layouts.items():
            for i in range(len(layout)):
                for j in range(len(layout[i])):
                    item_id = layout[i][j]
                    x, y = j * 64, i * 64
                    
                    if item_id != "-1":
                        if layer == "Floor":
                            pass
                        elif layer in ("Border", "Stone border", "Water", "Boss door"):
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                            
                        elif layer == "Trees":
                            if item_id in ("80", "81", "82", "83", "84", "85",
                                           "96", "97", "98", "99", "100", "101",
                                           "144", "145", "146", "147", "148", "149",
                                           "160", "161", "162", "163", "164", "165"):
                                Tile((x,y),[self.visible_sprites], "top layer", nature_textures[int(item_id)])
                            elif item_id in ("113", "116", "129", "132",
                                             "177", "180", "193", "196"):
                                Tile((x,y),[self.visible_sprites, self.obstacle_sprites], "obstacle", nature_textures[int(item_id)])
                            elif item_id in ("112", "114", "115", "117",
                                             "176", "178", "179", "181"):
                                Tile((x,y),[self.visible_sprites], "non obstacle", nature_textures[int(item_id)])
                            elif item_id in ("128", "130", "131", "133",
                                             "192", "194", "195", "197"):
                                Tile((x,y),[self.visible_sprites], "bottom layer", nature_textures[int(item_id)])
                                
                        elif layer == "Logs":
                            if item_id in ("86", "87", "102", "103", "150", "151", "152", "106", "107", "138", "139"):
                                Tile((x,y),[self.visible_sprites, self.obstacle_sprites], "obstacle", nature_textures[int(item_id)])
                            elif item_id in ("90", "91", "122", "123"):
                                Tile((x,y),[self.visible_sprites], "top layer", nature_textures[int(item_id)])
                                
                        elif layer == "Shrubs":
                            if item_id in ("134", "135", "136", "137"):
                                Tile((x,y),[self.visible_sprites, self.obstacle_sprites], "obstacle", nature_textures[int(item_id)])
                            elif item_id in ("104", "105", "118", "119", "120", "121"):
                                Tile((x,y),[self.visible_sprites], "top layer", nature_textures[int(item_id)])
                            elif item_id in ("88", "89"):
                                Tile((x,y),[self.visible_sprites], "non obstacle", nature_textures[int(item_id)])
                                
                        elif layer == "Objects":
                            if item_id in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "16", "17", "18"):
                                Tile((x,y),[self.visible_sprites, self.obstacle_sprites], "obstacle", nature_textures[int(item_id)])
                            
                            
                        elif layer == "Entities":
                            if item_id == "0":
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                            elif item_id == "1":
                                Ghost((x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites)
                            elif item_id == "2":
                                Sentry((x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites)
                            elif item_id == "3":
                                Bomber((x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites)
                                
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.visible_sprites.sprites() if sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            is_killed, projectile_direction = enemy.enemy_update(player)
            if is_killed and type(enemy) not in (Orb, Meteor):
                print(len(enemy_sprites) - 1, "enemies remain.")
            if projectile_direction:
                if type(enemy) == Sentry:
                    Orb(enemy.hitbox.center, projectile_direction, [self.visible_sprites, self.attackable_sprites])
                elif type(enemy) == Bomber:
                    Meteor(enemy.hitbox.center, projectile_direction, [self.visible_sprites, self.attackable_sprites])          
                                
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.shadow_offset = pygame.math.Vector2()
        self.shadow_offset.xy = 0, -8
        
        # 1:18:00
        self.floor_surface = pygame.image.load("../textures/tilemap/map_graphic.png").convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (80 * 64, 80 * 64))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        
        #print(self.sprites()[0].sprite_type)

        # THIS NEEDS TO BE REPLACED WITH A LAYERING SYSTEM
        #sprite_order_key = lambda sprite: sprite.rect.centery if sprite.sprite_type != "tree leaves" else sprite.rect.centery + 1000000
        def sprite_order_key(sprite):
            if sprite.sprite_type == "top layer":
                return sprite.rect.centery + 1000000
            elif sprite.sprite_type == "bottom layer":
                return sprite.rect.centery - 1000000
            return sprite.rect.centery
        
        bombers = []
        for sprite in sorted(self.sprites(), key=sprite_order_key):
            offset_pos = sprite.rect.topleft - self.offset
            if type(sprite) in (Player, Ghost, Sentry, Bomber):
                self.display_surface.blit(sprite.shadow, offset_pos - self.shadow_offset)
            if type(sprite) == Bomber:
                #offset_pos.y -= 200
                bombers.append(sprite)
            else:
                self.display_surface.blit(sprite.image, offset_pos)
            
        for bomber in bombers:
            offset_pos = bomber.rect.topleft - self.offset
            offset_pos.y -= 200
            self.display_surface.blit(bomber.image, offset_pos)


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
    
def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (64, 64))
            surface_list.append(image_surf)

    return surface_list