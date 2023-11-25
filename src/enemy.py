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
        self.rect = self.image.get_rect(topleft=position)
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

    
    def import_textures(self) -> None:
        raise NotImplementedError()


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
        raise NotImplementedError()

        
    def actions(self, player: Player):
        raise NotImplementedError()


    def animate(self):
        raise NotImplementedError()


    def cooldown(self):
        raise NotImplementedError()
    
    
    def player_attack_update(self, player: Player) -> None:
        player_distance, player_direction = self.get_entity_distance_direction(player)
        if player_distance < player.attack_distance:
            if player.is_attacking:
                if player_distance < 10 or self.get_reversed_direction(player.get_direction_facing()) * player_direction >= 0.5: 
                    self.health -= player.attack_damage
        
        
    def boomerang_attack_update(self, player: Player) -> None:
        if player.boomerang and self.enemy_name != "boomerang":    
            boomerang_distance, boomerang_direction = self.get_entity_distance_direction(player.boomerang)
            if boomerang_distance < player.boomerang.attack_distance: 
                self.health -= player.boomerang.attack_damage
                player.boomerang.max_age = 0
                    
    
    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        self.cooldown()


    # Returns whether or not the sprite has been killed and the direction of a launched orb.
    def enemy_update(self, player):
        self.update_status(player)
        projectile_direction = self.player_attack_update(player)
        self.boomerang_attack_update(player)
        is_killed = False
        if self.health <= 0:
            self.kill()
            is_killed = True        
        return (is_killed, projectile_direction)