import pygame
from entity import Entity
from player import Player
from enemy import Enemy


class Bomber(Enemy):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__("bomber", position, groups, layer_num, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/bomber/0.png")
        self.display_image = self.image.copy()
        
        self.import_textures()
        self.status = "stand"
        self.animation_speed = 0.2

        self.health = 5
        self.speed = 5
        self.attack_damage = 0
        self.attack_radius = 10
        self.notice_radius = 500

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 4000
        
        self.damage_sound = pygame.mixer.Sound("../audio/mixkit-weak-fast-blow-2145.wav")
        self.damage_sound.set_volume(0.5)
        
        self.killed_sound = pygame.mixer.Sound("../audio/mixkit-video-game-power-up-3164.wav")
        self.killed_sound.set_volume(0.5)
        
    
    def import_textures(self) -> None:
        path = "../textures/entities/bomber/"
        self.textures = [
            self.get_texture_surface(path + "0.png"),
            self.get_texture_surface(path + "1.png"),
            self.get_texture_surface(path + "2.png"),
        ]
        
        
    def update_status(self, player: Player) -> None:
        player_distance, player_direction = self.get_entity_distance_direction(player)

        if player_distance > self.notice_radius or player.health <= 0:
            self.direction.xy = 0, 0
            self.status = "stand"

        else:
            self.direction = player_direction
            self.status = self.get_direction_str()
            
            
    def animate(self) -> None:
        animation = self.textures
   
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        self.display_image = self.image.copy()
        if self.damage_taken:
            self.display_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
            self.damage_taken = False
        
        
    def player_attack_update(self, player: Player) -> None:
        player_distance, player_direction = self.get_entity_distance_direction(player)
        if player_distance < self.attack_radius and self.can_attack and player.health > 0:
            self.attack_time = pygame.time.get_ticks()
            self.can_attack = False
            return player_direction
        else:
            return None
        
        
    def boomerang_attack_update(self, player: Player) -> None:
        if player.boomerang:  
            original_position = self.rect.center
            self.rect.center = (original_position[0], original_position[1] - 200)
            boomerang_distance, boomerang_direction = self.get_entity_distance_direction(player.boomerang)
            self.rect.center = original_position
            if boomerang_distance < player.boomerang.attack_distance: 
                self.take_damage(player.boomerang.attack_damage)
                player.boomerang.max_age = 0
        
        
    def cooldown(self) -> None:
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True




    