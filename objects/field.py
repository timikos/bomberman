import pygame
from constants import FieldProperties, Color
from objects.base import DrawObject


class Field(DrawObject):
    def __init__(self, game, x=0, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.field = []
        self.width = width  # Ширина поля в клетках
        self.height = height  # Высота поля в клетках
        self.x = x
        self.y = y
        for y in range(height):
            self.field += [[]]
            for x in range(width):
                self.field[-1].append(Cell(game, x * FieldProperties.CELL_LENGTH + self.x,
                                           y * FieldProperties.CELL_LENGTH + self.y, 'images/ground.png'))

    def process_draw(self):
        for i in self.field:
            for cell in i:
                cell.process_draw()

    def get_cell_by_pos(self, x, y):
        n = (x - self.x) // FieldProperties.CELL_LENGTH
        m = (y - self.y) // FieldProperties.CELL_LENGTH
        return self.field[n][m]


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
