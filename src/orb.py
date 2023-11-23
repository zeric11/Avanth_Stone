import pygame
from entity import Entity
from player import Player
from enemy import Enemy


class Orb(Enemy):
    def __init__(self, 
                 position: tuple[int, int], 
                 direction: pygame.math.Vector2,
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__("orb", position, groups, layer_num, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/orb.png")
        self.image = pygame.transform.scale(self.image, (32, 32))

        self.health = 1
        self.speed = 10
        self.attack_damage = 10
        self.attack_distance = 25
        self.notice_radius = 0
        self.direction = direction
        self.age = pygame.time.get_ticks()
        self.max_age = 1000000

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 0
        
        
    def get_status(self, player: Player) -> None:
        pass
            
            
    def animate(self) -> None:
        self.rect = self.image.get_rect(center=self.hitbox.center)
                
                
    def player_attack_update(self, player: Player) -> None:
        player_distance, player_direction = self.get_player_distance_direction(player)
        
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.health = 0
                    
        if player_distance < self.attack_distance:
            if player.is_blocking and self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5:
                player.knock_back(10, 10, player_direction)

            else:
                player.health -= self.attack_damage
                player.knock_back(10, 10, player_direction)
                pygame.time.get_ticks()
            self.health = 0
            
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        if self.max_age - self.age < 0:
            self.health = 0
        
