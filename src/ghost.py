import pygame
from entity import Entity
from player import Player
from enemy import Enemy


class Ghost(Enemy):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__("ghost", position, groups, layer_num, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/ghost/down/stand.png")
        
        self.import_textures()
        self.status = "down_stand"

        self.health = 100
        self.speed = 2
        self.attack_damage = 10
        self.attack_distance = 5
        self.notice_radius = 500

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        
        self.damage_sound = pygame.mixer.Sound("../audio/mixkit-explainer-video-game-alert-sweep-236.wav")
        self.damage_sound.set_volume(1)
        
        self.killed_sound = pygame.mixer.Sound("../audio/mixkit-failure-arcade-alert-notification-240.wav")
        
    
    def import_textures(self) -> None:
        path = "../textures/entities/ghost/"

        down_stand = self.get_texture_surface(path + "down/stand.png")
        up_stand = self.get_texture_surface(path + "up/stand.png")
        left_stand = self.get_texture_surface(path + "left/stand.png")
        right_stand = self.get_texture_surface(path + "right/stand.png")

        self.textures = {
            "down_stand": [down_stand],
            "down_attack": [self.get_texture_surface(path + "down/attack.png")],
            "down": [self.get_texture_surface(path + "down/step_1.png"), down_stand,
                     self.get_texture_surface(path + "down/step_2.png"), down_stand],

            "up_stand": [up_stand],
            "up_attack": [self.get_texture_surface(path + "up/attack.png")],
            "up": [self.get_texture_surface(path + "up/step_1.png"), up_stand,
                   self.get_texture_surface(path + "up/step_2.png"), up_stand],

            "left_stand": [left_stand],
            "left_attack": [self.get_texture_surface(path + "left/attack.png")],
            "left": [self.get_texture_surface(path + "left/step_1.png"), left_stand,
                     self.get_texture_surface(path + "left/step_2.png"), left_stand],

            "right_stand": [right_stand],
            "right_attack": [self.get_texture_surface(path + "right/attack.png")],
            "right": [self.get_texture_surface(path + "right/step_1.png"), right_stand,
                      self.get_texture_surface(path + "right/step_2.png"), right_stand],
        }
        
        
    def get_status(self, player: Player) -> None:
        player_distance, player_direction = self.get_player_distance_direction(player)

        if player_distance > self.notice_radius or player.health <= 0:
            self.direction.xy = 0, 0
            self.status = "down"

        else:
            self.direction = player_direction
            self.status = self.get_direction_str()
            
            
    def animate(self) -> None:
        animation = self.textures[self.status]
   
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        
    def cooldown(self) -> None:
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                
                
    def player_attack_update(self, player: Player) -> None:
        player_distance, player_direction = self.get_player_distance_direction(player)
        
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.take_damage(player.attack_damage)
                    self.knock_back(10, 10, self.get_reversed_direction(player_direction))
                    
        if player_distance < self.attack_distance and self.can_attack and player.health > 0:
            if player.is_blocking and self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5:
                player.block_damage()
                player.knock_back(10, 10, player_direction)
                self.knock_back(10, 5, self.get_reversed_direction(player_direction))
            else:
                player.take_damage(self.attack_damage)
                player.knock_back(10, 10, player_direction)
                
            self.attack_time = pygame.time.get_ticks()
            self.can_attack = False
            
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        self.cooldown()

    