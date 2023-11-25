import pygame
from entity import Entity
from player import Player
from enemy import Enemy


class Sentry(Enemy):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__("sentry", position, groups, layer_num, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/sentry/down.png")
        
        self.import_textures()
        self.status = "down"

        self.health = 100
        self.speed = 0
        self.attack_damage = 0
        self.attack_radius = 1000
        self.notice_radius = 1000

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 5000
        
    
    def import_textures(self) -> None:
        path = "../textures/entities/sentry/"
        self.textures = {
            "down" : self.get_texture_surface(path + "down.png"),
            "up" : self.get_texture_surface(path + "up.png"),
            "left" : self.get_texture_surface(path + "left.png"),
            "right" : self.get_texture_surface(path + "right.png"),
        }
        
        
    def update_status(self, player: Player) -> None:
        player_distance, player_direction = self.get_entity_distance_direction(player)

        if player_distance > self.notice_radius:
            self.direction.xy = 0, 0
            self.status = "down"

        else:
            self.direction = player_direction
            self.status = self.get_direction_str()
            
            
    def animate(self) -> None:
        self.image = self.textures[self.status]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        
    def cooldown(self) -> None:
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                
                
    def player_attack_update(self, player) -> pygame.math.Vector2:
        player_distance, player_direction = self.get_entity_distance_direction(player)
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.health -= player.attack_damage
                    
        if player_distance < self.attack_radius and self.can_attack:
            self.attack_time = pygame.time.get_ticks()
            self.can_attack = False
            return player_direction
        else:
            return None
                    
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        self.cooldown()

