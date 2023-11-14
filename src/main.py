import sys, pygame
from level import Level


S_WIDTH = 1000
S_HEIGHT = 800
FPS = 60


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption("The Avanth Stone")
    clock = pygame.time.Clock()

    level = Level()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("green")
        level.run()
        pygame.display.update()
        clock.tick(FPS)
