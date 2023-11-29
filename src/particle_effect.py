import pygame
from entity import Entity


class ParticleEffect(Entity):
    def __init__(self, 
                 particle_name: str,
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int) -> None:

        super().__init__(position, groups, "particle effect", layer_num)
        self.display_image = pygame.Surface((64, 64))
        self.rect = self.display_image.get_rect(topleft=position)
        self.textures = None
        self.frame_index = 0
        self.animation_speed = 0.5
        self.is_finished = False
        
        
    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.textures):
            self.is_finished = True
        else:
            self.display_image = self.textures[int(self.frame_index)]
            self.rect = self.display_image.get_rect(center = self.hitbox.center)
            
            
    def update(self) -> bool:
        self.animate()
        if self.is_finished:
            self.kill()
            return True
        return False