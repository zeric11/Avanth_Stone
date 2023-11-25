import pygame
from tile import Tile

class Entity(Tile):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 sprite_type: str, 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__(position, groups, "entity", layer_num)
        self.sprite_type = sprite_type
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0
        self.animation_speed = 0.08
        self.direction = pygame.Vector2()
        self.status = None
        self.shadow = self.get_texture_surface("../textures/entities/shadow.png")
        self.knock_back_amount = 0
        self.knock_back_speed = 0
        self.knock_back_direction = 0

    
    def move(self, speed: float) -> None:
        if self.knock_back_amount > 0:
            self.move_direction(self.knock_back_speed, self.knock_back_direction)
            self.knock_back_amount -= 1
            if self.knock_back_amount == 0:
                self.knock_back_speed = 0
                self.knock_back_direction = 0
        else:
            self.move_direction(speed, self.direction)

        
    def knock_back(self, duration: int, intensity: int, direction: pygame.math.Vector2) -> None:
        self.knock_back_amount = duration
        self.knock_back_speed = intensity
        self.knock_back_direction = direction
    
    
    def move_direction(self, speed: float, direction: pygame.math.Vector2) -> None:
        if direction.magnitude() != 0:
            direction = direction.normalize()
        self.hitbox.x += direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center


    def collision(self, direction: pygame.math.Vector2) -> None:
        if direction == "horizontal" and self.obstacle_sprites:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        elif direction == "vertical" and self.obstacle_sprites:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom


    def get_texture_surface(self, path: str) -> pygame.Surface:
        surface = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(surface, (64, 64))
    

    def remove_actions(self) -> None:
        if "stand" in self.status:
                self.status = self.status.replace("_stand", "")
        if "attack" in self.status:
                self.status = self.status.replace("_attack", "")
        if "block" in self.status:
                self.status = self.status.replace("_block", "")
                
                
    def get_normalized_direction(self, direction: pygame.math.Vector2) -> pygame.math.Vector2:
        normalized_direction = pygame.math.Vector2()
        if abs(direction.x) > abs(direction.y):
            normalized_direction.xy = direction.x, 0
        else:
            normalized_direction.xy = 0, direction.y
        if normalized_direction.x != 0 or normalized_direction.y != 0:
            normalized_direction.normalize()
        return normalized_direction
    
    
    def get_reversed_direction(self, direction: pygame.math.Vector2) -> pygame.math.Vector2:
        reversed_direction = pygame.math.Vector2()
        reversed_direction.x = -direction.x if direction.x != 0 else 0
        reversed_direction.y = -direction.y if direction.y != 0 else 0
        return reversed_direction


    def get_direction_str(self) -> str:
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
            
            
             
            