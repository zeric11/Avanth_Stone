import sys, pygame
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")
        level.run()
        pygame.display.update()
        clock.tick(FPS)
