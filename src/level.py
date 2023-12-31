import pygame
from player import Player
from boomerang import Boomerang
from enemy import Enemy
from ghost import Ghost
from sentry import Sentry
from orb import Orb
from bomber import Bomber
from meteor import Meteor
from explosion_effect import ExplosionEffect
from killed_effect import KilledEffect
from tile import *


class Level:
    def __init__(self) -> None:

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()
        
        self.level_finished = False
        self.is_killed = False
        self.time_killed = 0
        self.time_before_finished = 2000


    # Returns where player has died or not.
    def run(self) -> None:
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.draw_hearts()
        self.draw_score()
        self.update()
        self.enemy_update()
        self.boomerang_update()
        if pygame.key.get_pressed()[pygame.K_k]:
            self.kill_all_enemies()
        if self.player.health <= 0 and self.time_killed == 0:
            self.is_killed = True
            self.time_killed = pygame.time.get_ticks()
        if self.is_killed and pygame.time.get_ticks() - self.time_killed >= self.time_before_finished:
            self.level_finished = True
        return self.level_finished

    
    def create_map(self) -> None:
        self.ui_textures = import_folder("../textures/ui")
        textures = import_folder("../textures/nature")
        for layer, layout in layouts.items():
            for i in range(len(layout)):
                for j in range(len(layout[i])):
                    tile_id = int(layout[i][j])
                    if tile_id != -1: 
                        self.load_sprite(layer, tile_id, (j * 64, i * 64), textures)
                                
                                
    def load_sprite(self, layer: str, tile_id: int, position: tuple[int, int], textures) -> None:
        global tilemap_indices
        
        if layer == "Floor":
            pass
        
        elif layer in ("Border", "Stone border", "Water", "Boss door frame"):
            Tile(position, [self.obstacle_sprites], "border", layer_num=1)
            
        elif layer == "Boss door":
            image_surf = pygame.image.load("../textures/tilemap/wooden_door_closed.png").convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (64, 64))
            self.boss_door = Tile(position, [self.visible_sprites, self.obstacle_sprites], "closed boss door", layer_num=1, surface=image_surf)
            
        elif layer == "Trees":
            if tile_id in tilemap_indices["objects - tree leaves"]:
                Tile(position, [self.visible_sprites], "tree leaves", layer_num=2, surface=textures[tile_id])
                
            elif tile_id in tilemap_indices["objects - tree trunks"]:
                Tile(position, [self.visible_sprites, self.obstacle_sprites], "tree trunk", layer_num=1, surface=textures[tile_id])
            
            elif tile_id in tilemap_indices["objects - tree side leaves"]:
                Tile(position, [self.visible_sprites], "non obstacle", layer_num=1, surface=textures[tile_id])
            
            elif tile_id in tilemap_indices["objects - tree sides"]:
                Tile(position, [self.visible_sprites], "bottom layer", layer_num=0, surface=textures[tile_id])
                
        elif layer == "Logs":
            if tile_id in tilemap_indices["objects - log bottoms"]:
                Tile(position, [self.visible_sprites, self.obstacle_sprites], "obstacle", layer_num=1, surface=textures[tile_id])
                
            elif tile_id in tilemap_indices["objects - log tops"]:
                Tile(position, [self.visible_sprites], "top layer", layer_num=2, surface=textures[tile_id])
                
        elif layer == "Shrubs":
            if tile_id in tilemap_indices["objects - shrub bottoms"]:
                Tile(position, [self.visible_sprites, self.obstacle_sprites], "obstacle", layer_num=1, surface=textures[tile_id])
                
            elif tile_id in tilemap_indices["objects - shrub tops"]:
                Tile(position, [self.visible_sprites], "top layer", layer_num=2, surface=textures[tile_id])
                
            elif tile_id in tilemap_indices["objects - saplings"]:
                Tile(position, [self.visible_sprites], "non obstacle", layer_num=1, surface=textures[tile_id])
                
        elif layer == "Objects":
            if tile_id in tilemap_indices["objects - items"]:
                Tile(position, [self.visible_sprites, self.obstacle_sprites], "obstacle", layer_num=1, surface=textures[tile_id])
            
        elif layer == "Entities":
            if tile_id == tilemap_indices["entities - player"]:
                self.player = Player(position, [self.visible_sprites], layer_num=1, obstacle_sprites=self.obstacle_sprites)
            elif tile_id == tilemap_indices["entities - ghost"]:
                Ghost(position, [self.visible_sprites, self.attackable_sprites], layer_num=1, obstacle_sprites=self.obstacle_sprites)
            elif tile_id == tilemap_indices["entities - sentry"]:
                Sentry(position, [self.visible_sprites, self.attackable_sprites], layer_num=1, obstacle_sprites=self.obstacle_sprites)
            elif tile_id == tilemap_indices["entities - bomber"]:
                Bomber(position, [self.visible_sprites, self.attackable_sprites], layer_num=3)
    
    
    def update(self) -> None:
        if self.boss_door.sprite_type == "opened boss door":
            if (pygame.math.Vector2(self.boss_door.rect.center) - pygame.math.Vector2(self.player.rect.center)).magnitude() < 10:
                self.level_finished = True
        for sprite in self.visible_sprites:
            is_killed = sprite.update()
            if is_killed:
                if type(sprite) == Meteor:
                    ExplosionEffect((sprite.hitbox.x, sprite.hitbox.y + 10), [self.visible_sprites], layer_num=1)
                elif type(sprite) in (Player, Ghost, Sentry):
                    KilledEffect((sprite.hitbox.x, sprite.hitbox.y + 10), [self.visible_sprites], layer_num=1)
                elif type(sprite) == Bomber:
                    KilledEffect((sprite.hitbox.x, sprite.hitbox.y - 200), [self.visible_sprites], layer_num=1)
              
                                
    def enemy_update(self) -> None:
        enemy_sprites = [sprite for sprite in self.visible_sprites.sprites() if sprite.sprite_type == "enemy"]
        if len(enemy_sprites) == 0:
            self.open_boss_door()
        for enemy in enemy_sprites:
            projectile_direction = enemy.enemy_update(self.player)
            if projectile_direction:
                if type(enemy) == Sentry:
                    Orb(enemy.hitbox.center, projectile_direction, [self.visible_sprites, self.attackable_sprites], layer_num=1)
                elif type(enemy) == Bomber:
                    Meteor(enemy.hitbox.center, projectile_direction, [self.visible_sprites, self.attackable_sprites], layer_num=1)
                    
                    
    def boomerang_update(self) -> None:
        if self.player.boomerang_staged and not self.player.boomerang_thrown:
            self.player.boomerang = Boomerang(
                (self.player.hitbox.center[0] - 30, self.player.hitbox.center[1] - 10), 
                self.player.get_direction_facing(), 
                [self.visible_sprites, self.attackable_sprites], 
                layer_num=3
            )
            self.player.boomerang_staged = False
            self.player.boomerang_thrown = True
            
            
    def kill_all_enemies(self) -> None:
        enemy_sprites = [sprite for sprite in self.visible_sprites.sprites() if sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.kill()
                    
                    
    def draw_hearts(self) -> None:
        for i in range(10):
            heart_surface = pygame.transform.scale(self.ui_textures[11 if self.player.health - i > 0 else 10], (32, 32))
            self.display_surface.blit(heart_surface, (4 + (i * 38), 4))
            
            
    def draw_score(self) -> None:
        enemies_remaining = len([sprite for sprite in self.visible_sprites.sprites() if type(sprite) in (Ghost, Sentry, Bomber)])
        enemies_remaining_str = str(enemies_remaining)
        digit_amount = len(enemies_remaining_str)
        for i in range(digit_amount):
            digit_surface = self.ui_textures[int(enemies_remaining_str[digit_amount - 1 - i])]
            digit_surface = pygame.transform.scale(digit_surface, (32, 32))
            self.display_surface.blit(digit_surface, (1920 - 32 - (i * 32), 4))
            
            
    def open_boss_door(self) -> None:
        image_surf = pygame.image.load("../textures/tilemap/wooden_door_open.png").convert_alpha()
        image_surf = pygame.transform.scale(image_surf, (64, 64))
        self.new_boss_door = Tile(self.boss_door.position, [self.visible_sprites], "opened boss door", layer_num=1, surface=image_surf)
        self.boss_door.kill()
        self.boss_door = self.new_boss_door
                                
                                
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.shadow_offset = pygame.math.Vector2()
        self.shadow_offset.xy = 0, -8
        
        self.floor_surface = pygame.image.load("../textures/tilemap/map_graphic.png").convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (80 * 64, 80 * 64))
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))


    def custom_draw(self, player: Player) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        
        def sprite_order_key(sprite):
            return sprite.rect.centery + (sprite.layer_num * 1000000)
        
        # Draw entity shadows first...
        for sprite in self.sprites():
            if type(sprite) in (Player, Ghost, Sentry, Bomber):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.shadow, offset_pos - self.shadow_offset)
                
        # Then draw everything else.
        for sprite in sorted(self.sprites(), key=sprite_order_key):
            offset_pos = sprite.rect.topleft - self.offset
            # Bomber needs to appear high above its shadow.
            if type(sprite) == Bomber:
                offset_pos.y -= 200
            self.display_surface.blit(sprite.display_image, offset_pos)
            
                
            
        

