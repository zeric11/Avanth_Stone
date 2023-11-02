import pygame
from entity import Entity


class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.enemy_name = name
        self.image = self.get_texture_surface("../textures/entities/ghost/down/stand.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        self.import_textures(name)
        self.status = "down_stand"

        self.health = 100
        self.speed = 2
        self.attack_damage = 10
        self.attack_radius = 50
        self.notice_radius = 500

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

    
    def import_textures(self, name):
        path = "../textures/entities/" + name + "/"

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
        distance = self.get_player_distance_direction(player)[0]

        # NEED TO FIX DIRECTIONAL STATUS
        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "down_attack"
        elif distance <= self.notice_radius:
            self.status = "down"
        else:
            self.status = "down_stand"

        
    def actions(self,player):
        # NEED TO FIX DIRECTIONAL STATUS
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
        elif self.status == "down":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()


    def animate(self):
        animation = self.textures[self.status]
   
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


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)