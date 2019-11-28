"""
Класс Background

Описание: данный класс реализует оформление заднего фона главного меню
"""
import pygame
from objects.base import DrawObject


class Background(DrawObject):
    filename = 'images/menu/main_menu.png'

    def __init__(self, game, location):
        super().__init__(game)
        self.image = pygame.image.load(self.filename)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location  # Координаты начала фона

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
