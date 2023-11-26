import pygame
from entity import Entity
from player import Player
from enemy import Enemy


class Meteor(Enemy):
    def __init__(self, 
                 position: tuple[int, int], 
                 direction: pygame.math.Vector2,
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        starting_position = pygame.Vector2()
        starting_position.xy = position[0] - 30, position[1] - 200
        super().__init__("meteor", starting_position, groups, layer_num, obstacle_sprites)
        self.image = self.get_texture_surface("../textures/entities/meteor/0.png")
        self.display_image = self.image.copy()
        self.import_textures()
        self.animation_speed = 0.15
        self.final_position = position

        self.health = 1
        self.speed = 2
        self.attack_damage = 2
        self.attack_distance = 15
        self.notice_radius = 0
        #self.direction = direction
        self.direction.xy = 0, 1
        self.age = pygame.time.get_ticks()
        self.max_age = 1000000

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 0
        
        self.killed_sound = pygame.mixer.Sound("../audio/mixkit-8-bit-bomb-explosion-2811.wav")
        self.killed_sound.set_volume(0.1)
        
        self.idle_sound = pygame.mixer.Sound("../audio/mixkit-long-game-over-notification-276.wav")
        self.idle_sound.set_volume(0.1)
        
        
    def import_textures(self) -> None:
        path = "../textures/entities/meteor/"
        self.textures = [
            self.get_texture_surface(path + "0.png"),
            self.get_texture_surface(path + "1.png"),
            self.get_texture_surface(path + "2.png"),
            self.get_texture_surface(path + "3.png"),
        ]
    
        
    def get_status(self, player: Player) -> None:
        pass
            
            
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
                
                
    def player_attack_update(self, player: Player) -> None:
        player_distance, player_direction = self.get_player_distance_direction(player)
        
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.health = 0
                    
        if player_distance < self.attack_distance:
            if player.is_blocking and self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5:
                player.block_damage()
                player.knock_back(10, 10, player_direction)

            else:
                player.take_damage(self.attack_damage)
                player.knock_back(10, 10, player_direction)
                
            self.health = 0
            
        elif self.hitbox.center[1] >= self.final_position[1]:
            self.health = 0
            

            


        

