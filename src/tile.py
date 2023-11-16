import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((64, 64))):
        # NEED TO ADD A LAYER FIELD AND IMPLEMENT A HANDLER IN custom_draw
        pygame.sprite.Sprite.__init__(self, groups)
        self.sprite_type = sprite_type
        self.image = surface
        #self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        
