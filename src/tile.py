import pygame
from csv import reader
from os import walk


def import_csv_layout(path: str) -> list[str]:
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map
    
    
def import_folder(path: str) -> list[pygame.Surface]:
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (64, 64))
            surface_list.append(image_surf)
    return surface_list


layouts = {
    "Entities" : import_csv_layout("../map/map_Entities.csv"),
    "Objects" : import_csv_layout("../map/map_Objects.csv"),
    "Decor" : import_csv_layout("../map/map_Decor.csv"),
    "Shrubs" : import_csv_layout("../map/map_Shrubs.csv"),
    "Logs" : import_csv_layout("../map/map_Logs.csv"),
    "Trees" : import_csv_layout("../map/map_Trees.csv"),
    "Boss door" : import_csv_layout("../map/map_Boss door.csv"),
    "Boss door frame" : import_csv_layout("../map/map_Boss door frame.csv"),
    "Water" : import_csv_layout("../map/map_Water.csv"),
    "Stone border" : import_csv_layout("../map/map_Stone border.csv"),
    "Border" : import_csv_layout("../map/map_Border.csv"),
    "Floor" : import_csv_layout("../map/map_Floor.csv"),
}


tilemap_indices = {
    "objects - tree leaves" : (80, 81, 82, 83, 84, 85,
                               96, 97, 98, 99, 100, 101,
                               144, 145, 146, 147, 148, 149,
                               160, 161, 162, 163, 164, 165),

    "objects - tree trunks" : (113, 116, 129, 132, 177, 180, 193, 196),
    "objects - tree side leaves" : (112, 114, 115, 117, 176, 178, 179, 181),
    "objects - tree sides" : (128, 130, 131, 133, 192, 194, 195, 197),

    "objects - log bottoms" : (86, 87, 102, 103, 150, 151, 152, 106, 107, 138, 139),
    "objects - log tops" : (90, 91, 122, 123),

    "objects - shrub bottoms" : (134, 135, 136, 137),
    "objects - shrub tops" : (104, 105, 118, 119, 120, 121),
    "objects - saplings" : (88, 89),

    "objects - items" : (0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18),

    "entities - player" : 0,
    "entities - ghost" : 1,
    "entities - sentry" : 2,
    "entities - bomber" : 3,
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 sprite_type: str, 
                 layer_num: int, 
                 surface=pygame.Surface((64, 64))) -> None:
        
        pygame.sprite.Sprite.__init__(self, groups)
        self.position = position
        self.sprite_type = sprite_type
        self.layer_num = layer_num
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.display_image = self.image
        self.hitbox = self.rect.inflate(-10, -20)



