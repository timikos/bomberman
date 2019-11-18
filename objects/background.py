import pygame
from objects.base import DrawObject


class Background(DrawObject):

    def __init__(self, game, image_file, location):
        super().__init__(game)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
