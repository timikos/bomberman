"""
Класс Door

Описание: данный класс позволяет реализовать дверь для прохождения уровня
"""
import pygame
from objects.base import DrawObject
from constants import FieldProperties
from Global import Globals


class Door(DrawObject):
    """Дверь"""
    filename = 'images/door/door.png'

    def __init__(self, game, hidden=True, x=20, y=80):
        super().__init__(game)
        self.image = pygame.image.load(Door.filename)
        self.hidden = hidden
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, FieldProperties.CELL_LENGTH, FieldProperties.CELL_LENGTH - 5)

    def collides_with(self, other):
        """Коллизия с объектом"""
        return self.rect.colliderect(other)

    def update_x(self, x):
        self.rect.x = self.x - x

    def show_door(self):
        """Открытие двери"""
        self.hidden = False
        self.rect.x = FieldProperties.CELL_LENGTH + 2

    def process_logic(self):
        pass

    def process_draw(self):
        self.update_x(Globals.FieldPosition - 860)
        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)
