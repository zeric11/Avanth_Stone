import pygame
from entity import Entity
from player import Player


class Enemy(Entity):
    def __init__(self, 
                 name: str,
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__(position, groups, "enemy", layer_num)
        self.enemy_name = name
        self.image = pygame.Surface((64, 64))
        self.display_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        self.status = None

        self.health = 0
        self.speed = 0
        self.attack_damage = 0
        self.attack_radius = 0
        self.notice_radius = 0

        # player interaction
        self.can_attack = False
        self.attack_time = None
        self.attack_cooldown = 0
        self.damage_taken = False
        self.stun_amount = 50
        self.stun_remaining = 0
        
        self.damage_sound = None
        self.idle_sound = None
        self.killed_sound = None

    
    def import_textures(self) -> None:
        pass


    def get_entity_distance_direction(self, entity: Entity) -> tuple[pygame.math.Vector2, pygame.math.Vector2]:
        enemy_vec = pygame.math.Vector2(self.rect.center)
        entity_vec = pygame.math.Vector2(entity.rect.center)
        distance = (entity_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (entity_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)


    def update_status(self, player: Player) -> None:
        pass

        
    def actions(self, player: Player) -> None:
       pass


    def animate(self):
        self.damage_taken = False


    def cooldown(self):
        pass
    
    
    def killed_update(self):
        if self.health <= 0:
            if self.idle_sound:
                self.idle_sound.stop()
            if self.killed_sound:
                self.killed_sound.play()
    
    
    def take_damage(self, damage_amount: float) -> None:
        if self.stun_remaining <= 0:
            self.health -= damage_amount
            self.damage_taken = True
            self.stun_remaining = self.stun_amount
            if self.damage_sound and self.damage_sound.get_num_channels() < 1:
                self.damage_sound.play()
            
            
    def play_idle_sound(self) -> None:
        if self.idle_sound and self.idle_sound.get_num_channels() < 1:
            self.idle_sound.play()
    
    
    def player_attack_update(self, player: Player) -> None:
        player_distance, player_direction = self.get_entity_distance_direction(player)
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.take_damage(player.attack_damage)
        
        
    def boomerang_attack_update(self, player: Player) -> None:
        if player.boomerang and self.enemy_name != "boomerang":    
            boomerang_distance, boomerang_direction = self.get_entity_distance_direction(player.boomerang)
            if boomerang_distance < player.boomerang.attack_distance: 
                self.take_damage(player.boomerang.attack_damage)
                player.boomerang.max_age = 0

                    
                    
    def move(self, speed: float) -> None:
        if self.knock_back_amount > 0:
            self.move_direction(self.knock_back_speed, self.knock_back_direction)
            self.knock_back_amount -= 1
            if self.knock_back_amount == 0:
                self.knock_back_speed = 0
                self.knock_back_direction = 0
        elif self.stun_remaining > 0:
            self.stun_remaining -= 1
        else:
            self.move_direction(speed, self.direction)
    
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.play_idle_sound()
        if self.health <= 0:
            self.killed_update()
            self.kill()   
            return True
        return False


    # Returns whether or not the sprite has been killed and the direction of a launched orb.
    def enemy_update(self, player):
        self.update_status(player)
        self.boomerang_attack_update(player)
        return self.player_attack_update(player)  
