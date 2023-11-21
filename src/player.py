import pygame
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = "player"
        self.image = self.get_texture_surface("../textures/entities/player/down/stand.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        self.import_player_textures()
        self.status = "down_stand"
        
        self.speed = 5
        self.blocking = False
        self.attacking = False
        self.attack_duration = 300
        self.attack_cooldown = 500
        self.attack_start_time = 0
        self.attack_end_time = 0


    def import_player_textures(self):
        path = "../textures/entities/player/"

        down_stand = self.get_texture_surface(path + "down/stand.png")
        up_stand = self.get_texture_surface(path + "up/stand.png")
        left_stand = self.get_texture_surface(path + "left/stand.png")
        right_stand = self.get_texture_surface(path + "right/stand.png")

        self.textures = {
            "down_stand": [down_stand],
            "down_attack": [self.get_texture_surface(path + "down/attack.png")],
            "down_block": [self.get_texture_surface(path + "down/block.png")],
            "down": [self.get_texture_surface(path + "down/step_1.png"), down_stand,
                     self.get_texture_surface(path + "down/step_2.png"), down_stand],

            "up_stand": [up_stand],
            "up_attack": [self.get_texture_surface(path + "up/attack.png")],
            "up_block": [self.get_texture_surface(path + "up/block.png")],
            "up": [self.get_texture_surface(path + "up/step_1.png"), up_stand,
                   self.get_texture_surface(path + "up/step_2.png"), up_stand],

            "left_stand": [left_stand],
            "left_attack": [self.get_texture_surface(path + "left/attack.png")],
            "left_block": [self.get_texture_surface(path + "left/block.png")],
            "left": [self.get_texture_surface(path + "left/step.png"), left_stand],

            "right_stand": [right_stand],
            "right_attack": [self.get_texture_surface(path + "right/attack.png")],
            "right_block": [self.get_texture_surface(path + "right/block.png")],
            "right": [self.get_texture_surface(path + "right/step.png"), right_stand],
        }

    

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.blocking = False

        # Abilities input
        if not self.attacking and keys[pygame.K_z]:
            self.attacking = True
            self.attack_start_time = pygame.time.get_ticks()

        if keys[pygame.K_x]:
            self.attacking = False
            self.blocking = True

        # Movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        else:
            self.direction.x = 0

        
    def get_status(self):
        if self.blocking:
            self.direction.x = 0
            self.direction.y = 0
            self.attacking = False
            if not "block" in self.status:
                if "stand" in self.status:
                    self.status = self.status.replace("_stand", "_block")
                elif "attack" in self.status:
                    self.status = self.status.replace("_attack", "_block")
                else:
                    self.status += "_block"

        elif self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "stand" in self.status:
                    self.status = self.status.replace("_stand", "_attack")
                elif "block" in self.status:
                    self.status = self.status.replace("_block", "_attack")
                else:
                    self.status += "_attack"

        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")
            if "block" in self.status:
                self.status = self.status.replace("_block", "")
            if self.direction.x == 0 and self.direction.y == 0 and "stand" not in self.status:
                self.status += "_stand"


    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking and current_time - self.attack_start_time >= self.attack_duration:
            self.attacking = False
            self.attack_end_time = pygame.time.get_ticks()

        if self.attacking and current_time - self.attack_end_time < self.attack_cooldown:
            self.attacking = False
            

    def animate(self):
        animation = self.textures[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
            
            
    def update(self):
        self.get_input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
