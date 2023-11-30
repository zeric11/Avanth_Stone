import sys
import pygame
from level import Level


S_WIDTH = 1920
S_HEIGHT = 1080
FPS = 60


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption("The Avanth Stone")
    clock = pygame.time.Clock()

    level = Level()
    
    main_sound = pygame.mixer.Sound("../audio/ForestWalk.mp3")
    main_sound.set_volume(0.5)
    main_sound.play(loops=-1)
    
    game_over_graphic = pygame.image.load("../textures/game_over_graphic.png").convert()
    game_over_graphic = pygame.transform.scale(game_over_graphic, (1080, 1080))
    
    level_finished = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        if not level_finished:
            screen.fill("black")
            level_finished = level.run()
            pygame.display.update()
        
        else:
            screen.fill("black")
            pygame.display.get_surface().blit(game_over_graphic, (420, 0))
            pygame.display.update()

        clock.tick(FPS)