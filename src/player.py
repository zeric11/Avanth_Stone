import pygame
from entity import Entity


class Player(Entity):
    def __init__(self, 
                 position: tuple[int, int], 
                 groups: list[pygame.sprite.Group], 
                 layer_num: int, 
                 obstacle_sprites=None) -> None:
        
        super().__init__(position, groups, "player", layer_num)
        self.image = self.get_texture_surface("../textures/entities/player/down/stand.png")
        self.display_image = self.image.copy()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -20)
        self.obstacle_sprites = obstacle_sprites

        self.import_player_textures()
        self.status = "down_stand"
        
        self.health = 10
        self.speed = 7
        self.is_blocking = False
        self.attack_damage = 2
        self.attack_distance = 100
        self.is_attacking = False
        self.attack_duration = 50
        self.attack_cooldown = 500
        self.attack_start_time = 0
        self.attack_end_time = 0
        
        self.boomerang = None
        self.boomerang_staged = False
        self.boomerang_thrown = False

        self.damage_taken = False
        
        self.attack_sound = pygame.mixer.Sound("../audio/mixkit-fast-sword-whoosh-2792.wav")
        self.attack_sound.set_volume(1)
        
        self.block_sound = pygame.mixer.Sound("../audio/mixkit-sword-pierces-armor-2761.wav")
        self.block_sound.set_volume(1)
        
        self.damage_sound = pygame.mixer.Sound("../audio/mixkit-knife-fast-hit-2184.wav")
        self.damage_sound.set_volume(1)
        
        self.killed_sound = pygame.mixer.Sound("../audio/mixkit-funny-system-break-down-2955.wav")


    def import_player_textures(self) -> None:
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


    # Returns true if boomerang was thrown
    def get_input(self) -> bool:
        keys = pygame.key.get_pressed()
        self.is_blocking = False

        # Abilities input
        if not self.is_attacking and keys[pygame.K_z]:
            self.is_attacking = True
            self.attack_start_time = pygame.time.get_ticks()

        if keys[pygame.K_x]:
            self.is_attacking = False
            self.is_blocking = True
            
        if not self.is_attacking and not self.is_blocking and keys[pygame.K_c]:
            self.boomerang_staged = True
            
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

        
    def get_status(self) -> None:
        if self.is_blocking:
            self.direction.x = 0
            self.direction.y = 0
            self.is_attacking = False
            
            self.remove_actions()
            self.status += "_block"

        elif self.is_attacking:
            self.direction.x = 0
            self.direction.y = 0

            self.remove_actions()
            self.status += "_attack"

        else:
            self.remove_actions()
            if self.direction.x == 0 and self.direction.y == 0:
                self.status += "_stand"
                
                
    def get_direction_facing(self) -> pygame.Vector2:
        if self.direction.x != 0 or self.direction.y != 0:
            return self.direction.copy()
        direction = pygame.math.Vector2()
        if "down" in self.status:
            direction.xy = 0, 1
        elif "up" in self.status:
            direction.xy = 0, -1
        elif "left" in self.status:
            direction.xy = -1, 0
        elif "right" in self.status:
            direction.xy = 1, 0
        return direction
         

    def cooldowns(self) -> None:
        current_time = pygame.time.get_ticks()

        if self.is_attacking and current_time - self.attack_start_time >= self.attack_duration:
            self.is_attacking = False
            self.attack_end_time = pygame.time.get_ticks()

        if current_time - self.attack_end_time < self.attack_cooldown:
            self.is_attacking = False
            

    def animate(self) -> None:
        animation = self.textures[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
        self.display_image = self.image.copy()
        if self.damage_taken:
            self.display_image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
            self.damage_taken = False
        
    
    
    def take_damage(self, damage_amount: float) -> None:
        self.health -= damage_amount
        self.damage_taken = True
        self.damage_sound.play()
        
        
    def block_damage(self) -> None:
        self.block_sound.play()
        
        
    def play_attack_sound(self) -> None:
        if self.is_attacking:
            if self.attack_sound.get_num_channels() < 1:
                self.attack_sound.play()
        else:
            if self.attack_sound.get_num_channels() > 0:
                self.attack_sound.stop()
                
                
    def killed_update(self):
        if self.health <= 0:
            self.killed_sound.play()
        
            
    def update(self) -> bool:
        self.get_input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.play_attack_sound()
        if self.health <= 0:
            self.killed_update()
            self.kill()
            return True        
        return False
    
        

