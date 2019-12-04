"""
Классы Field, Cell

Описание: данные классы реализуют заполнение полем экран игры
"""
import pygame
from constants import FieldProperties
from objects.base import DrawObject
from Global import Globals


class Field(DrawObject):
    """Поле"""
    def __init__(self, game, x=40, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT,
                 ground_texture='images/levels/ground_1_grass.png'):
        super().__init__(game)
        self.field = []
        self.filename = ground_texture
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        for y in range(height):
            self.field += [[]]  # Двумерный массив поля
            for x in range(width):
                self.field[-1].append(Cell(game, x * FieldProperties.CELL_LENGTH + self.x,
                                           y * FieldProperties.CELL_LENGTH + self.y, self.filename))

    def process_draw(self):
        for i in self.field:
            for cell in i:
                cell.update_x(Globals.FieldPosition-400)
                cell.process_draw()

    @staticmethod
    def get_cell_by_pos(x, y):
        """Получение центра координат клетки"""
        cell_x = (x + Globals.FieldPosition) // 40 * 40
        print(cell_x)
        cell_y = (y + 10) // 40 * 40
        return [cell_x, cell_y]


"""Клетка на поле"""
class Cell(DrawObject):
    def __init__(self, game, x, y, image):
        super().__init__(game)
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.rect.height = FieldProperties.CELL_LENGTH

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update_x(self,x):
        """Обновление позиции"""
        self.rect.x=self.x-x
