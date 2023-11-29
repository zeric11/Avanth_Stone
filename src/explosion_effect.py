import pygame
from particle_effect import ParticleEffect


class ExplosionEffect(ParticleEffect):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int) -> None:
        
        super().__init__("explosion effect", position, groups, layer_num)
        self.import_textures()
        self.display_image = self.textures[0]
        self.animation_speed = 0.3


    def import_textures(self) -> None:
        path = "../textures/effects/explosion/"
        self.textures = [
            self.get_texture_surface(path + str(i) + ".png") for i in range(6)
        ]
        
        