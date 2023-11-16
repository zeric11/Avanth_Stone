import pygame
from entity import Entity
from enemy import Enemy

class Sentry(Enemy):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__("sentry", pos, groups, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/sentry/down.png")
        
        self.import_textures()
        self.status = "down"

        self.health = 100
        self.speed = 0
        self.attack_damage = 0
        self.attack_radius = 0
        self.notice_radius = 500

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        
    
    def import_textures(self):
        path = "../textures/entities/sentry/"
        self.textures = {
            "down" : self.get_texture_surface(path + "down.png"),
            "up" : self.get_texture_surface(path + "up.png"),
            "left" : self.get_texture_surface(path + "left.png"),
            "right" : self.get_texture_surface(path + "right.png"),
        }
        
        
    def get_status(self, player):
        player_distance, player_direction = self.get_player_distance_direction(player)

        if player_distance > self.notice_radius:
            self.direction.xy = 0, 0
            self.status = "down"

        else:
            self.direction = player_direction
            self.status = self.get_direction_str()
            
            
    def animate(self):
        self.image = self.textures[self.status]
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
    #    #self.actions(player)
    