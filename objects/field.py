import pygame
from constants import FieldProperties, Color


class Field:
    def __init__(self, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        self.field = []
        self.width = width  # Ширина поля в клетках
        self.height = height  # Высота поля в клетках
        for y in range(height):
            self.field += [[]]
            for x in range(width):
                self.field[-1].append(Cell(x, y, 'images/ground.png'))

    def render(self, screen):
        screen.fill(Color.WHITE)
        for i in self.field:
            for cell in i:
                cell.render(screen)


class Cell:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x * FieldProperties.CELL_LENGTH
        self.rect.y = y * FieldProperties.CELL_LENGTH
        self.rect.width = self.rect.height = FieldProperties.CELL_LENGTH

    def render(self, screen):
        screen.blit(self.image, self.rect)
