import pygame
from checkers.game import Game
from checkers.constants import *


def main():

    # pygame setup
    pygame.init()

    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    game = Game(screen)

    pygame.display.flip()

    # flip() the display to put your work on screen
    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                (x, y) = pygame.mouse.get_pos()
                game.select(x, y)
                game.update(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game.undo(screen)

        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    main()
