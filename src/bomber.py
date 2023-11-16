import pygame
from entity import Entity
from enemy import Enemy

class Bomber(Enemy):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__("bomber", pos, groups, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/bomber/0.png")
        
        self.import_textures()
        self.status = "stand"
        self.animation_speed = 0.2

        self.health = 100
        self.speed = 2
        self.attack_damage = 10
        self.attack_radius = 50
        self.notice_radius = 500

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        
    
    def import_textures(self):
        path = "../textures/entities/bomber/"
        self.textures = [
            self.get_texture_surface(path + "0.png"),
            self.get_texture_surface(path + "1.png"),
            self.get_texture_surface(path + "2.png"),
        ]
        
    def get_status(self, player):
        player_distance, player_direction = self.get_player_distance_direction(player)

        if player_distance > self.notice_radius:
            self.direction.xy = 0, 0
            self.status = "stand"

        else:
            self.direction = player_direction
            self.status = self.get_direction_str()
            
            
    def animate(self):
        animation = self.textures
   
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        
    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    
    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()


    #def enemy_update(self, player):
    #    self.get_status(player)
    #   #self.actions(player)
    