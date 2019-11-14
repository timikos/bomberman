import sys

import pygame
from game import Game
from objects.field import Field
from constants import FieldProperties

if __name__ == '__main__':
    # g = Game()
    # g.main_loop()
    pygame.init()
    screen = pygame.display.set_mode((FieldProperties.WIDTH * FieldProperties.CELL_LENGTH,
                                      FieldProperties.HEIGHT * FieldProperties.CELL_LENGTH))
    game_over = False
    field = Field()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        field.render(screen)
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit(0)
