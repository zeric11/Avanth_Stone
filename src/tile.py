import pygame


class Tile(pygame.sprite.Sprite):
<<<<<<< Updated upstream
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/nature/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
=======
    def __init__(self, pos, groups, sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = pygame.image.load("../textures/nature/rock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
>>>>>>> Stashed changes
