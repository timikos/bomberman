import pygame
from constants import FieldProperties
from objects.base import DrawObject


class Field(DrawObject):

    @staticmethod
    def get_cell_by_pos(x, y):
        cell_x = (x + 10) // 40 * 40
        cell_y = (y + 10) // 40 * 40
        return [cell_x, cell_y]

    def __init__(self, game, x=40, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT, filename='images/levels/ground_1_grass.png'):
        super().__init__(game)
        self.field = []
        self.filename = filename
        self.width = width  # Ширина поля в клетках
        self.height = height  # Высота поля в клетках
        self.x = x
        self.y = y
        for y in range(height):
            self.field += [[]]
            for x in range(width):
                self.field[-1].append(Cell(game, x * FieldProperties.CELL_LENGTH + self.x,
                                           y * FieldProperties.CELL_LENGTH + self.y, self.filename))

    def process_draw(self):
        for i in self.field:
            for cell in i:
                cell.process_draw()



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
