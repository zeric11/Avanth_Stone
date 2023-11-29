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
        self.image = self.get_texture_surface("../textures/entities/boomerang.png")
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.display_image = self.image.copy()

        self.health = 1
        self.speed = 10
        self.attack_damage = 1
        self.attack_distance = 30
        self.notice_radius = 0
        self.direction = direction
        self.start_age = pygame.time.get_ticks()
        self.max_age = 1000
        self.angle = 0
        
        self.start_sound = pygame.mixer.Sound("../audio/zapsplat_cartoon_swipe_swish_throw_spinning_object_boomerang_001_101941.mp3")
        self.start_sound.set_volume(1)
        self.start_sound.play()
        
        self.killed_sound = pygame.mixer.Sound("../audio/zapsplat_leisure_boomerang_wooden_catch_single_hand_001_47807.mp3")
        self.killed_sound.set_volume(1)
        
        
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
        self.display_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.display_image.get_rect(center=self.hitbox.center)
        self.angle += 10
         
                
    def player_attack_update(self, player: Player) -> None:
        pass
            
    
        

