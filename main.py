import pygame
from checkers.game import Game
from checkers.constants import *


def main():

    # pygame setup
    pygame.init()

    # Define button properties
    button_color = GREEN
    button_rect = pygame.Rect(BOARD_WIDTH + 50, 100, 50, 50)
    button_text = "Click Me"
    font = pygame.font.Font(None, 36)

    def draw_button(screen, rect, color, text):
        pygame.draw.rect(screen, color, rect)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    screen = pygame.display.set_mode((BOARD_WIDTH + 200, BOARD_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    game = Game(screen)
    pygame.display.flip()

    # flip() the display to put your work on screen
    while running:
        pygame.display.flip()

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game.undo(screen)
                    pygame.display.flip()
                    continue

                (x, y) = pygame.mouse.get_pos()
                game.select(x, y)
                game.update(screen)

        draw_button(screen, button_rect, button_color, button_text)
        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == "__main__":
    main()
