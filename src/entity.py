import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.08
        self.direction = pygame.Vector2()
        self.status = None

    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom


    def get_texture_surface(self, path):
        surface = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(surface, (64, 64))
    

    def remove_actions(self):
        if "stand" in self.status:
                self.status = self.status.replace("_stand", "")
        if "attack" in self.status:
                self.status = self.status.replace("_attack", "")
        if "block" in self.status:
                self.status = self.status.replace("_block", "")


    def get_direction_str(self):
        if abs(self.direction.x) > abs(self.direction.y):
            if self.direction.x > 0:
                return "right"
            else:
                return "left"
        else:
            if self.direction.y > 0:
                return "down"
            else:
                return "up"
            
             
            