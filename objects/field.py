import pygame
from constants import FieldProperties, Color
from objects.base import DrawObject


class Field(DrawObject):
    def __init__(self, game, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.field = []
        self.width = width  # Ширина поля в клетках
        self.height = height  # Высота поля в клетках
        for y in range(height):
            self.field += [[]]
            for x in range(width):
                self.field[-1].append(Cell(game, x, y, 'images/ground.png'))

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
        self.rect.x = x * FieldProperties.CELL_LENGTH
        self.rect.y = y * FieldProperties.CELL_LENGTH
        self.rect.width = self.rect.height = FieldProperties.CELL_LENGTH

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
