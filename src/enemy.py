import pygame
from entity import Entity


class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites):
        super().__init__(pos, groups)
        self.sprite_type = "enemy"
        self.enemy_name = name
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        #self.import_textures(name)
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

    
    def import_textures(self):
        raise NotImplementedError()


    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)


    def get_status(self, player):
        raise NotImplementedError()

        
    def actions(self,player):
        raise NotImplementedError()


    def animate(self):
        raise NotImplementedError()


    def cooldown(self):
        raise NotImplementedError()
    
    
    def player_attack_update(self, player):
        player_distance, player_direction = self.get_player_distance_direction(player)
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.health -= player.attack_damage
                    
    
    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()


    # Returns whether or not the sprite has been killed.
    def enemy_update(self, player):
        self.get_status(player)
        self.player_attack_update(player)
        if self.health <= 0:
            self.kill()
            return True        
        return False