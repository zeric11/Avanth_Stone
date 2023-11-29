import pygame
from entity import Entity
from player import Player
from enemy import Enemy


class Boomerang(Enemy):
    def __init__(self, 
                 position: tuple[int, int], 
                 direction: pygame.math.Vector2,
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__("boomerang", position, groups, layer_num, obstacle_sprites)
        self.original_image = self.get_texture_surface("../textures/entities/boomerang.png")
        self.original_image = pygame.transform.scale(self.original_image, (48, 48))
        self.image = self.original_image.copy()

        self.health = 1
        self.speed = 10
        self.attack_damage = 10
        self.attack_distance = 30
        self.notice_radius = 0
        self.direction = direction
        self.start_age = pygame.time.get_ticks()
        self.max_age = 1000
        self.angle = 0
        
        
    def update_status(self, player: Player) -> None:
        if pygame.time.get_ticks() - self.start_age >= self.max_age:
            player_distance, player_direction = self.get_entity_distance_direction(player)
            self.direction = player_direction
            if player_distance < self.attack_distance:
                self.health = 0
                player.boomerang = None
                player.boomerang_staged = False
                player.boomerang_thrown = False
            
            
    def animate(self) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.angle += 10
         
                
    def player_attack_update(self, player: Player) -> None:
        pass
            
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        #if pygame.time.get_ticks() - self.start_age >= self.max_age:
        #    self.health = 0
        

