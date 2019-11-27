import pygame
from objects.base import DrawObject
from Global import Globals
from objects.field import Field


class RespawnPoint(DrawObject):
    def __init__(self, game, x=100, y=320, hidden=True, image='images/icon.png'):
        super().__init__(game)
        self.x, self.y = Field.get_cell_by_pos(x, y)
        # self.x = x
        # self.y = y
        self.hidden = hidden
        self.rect = pygame.Rect(self.x, self.y, 35, 35)
        self.image = pygame.image.load(image)

    def hide(self):
        self.hidden = True
        self.rect.x = 0
        self.rect.y = 0

    def collides_with(self, bomberman):
        return self.rect.colliderect(bomberman)

    def update_x(self, x):
        self.rect.x = self.x - x

    def process_draw(self):
        self.update_x(Globals.FieldPosition - 400)
        if not self.hidden:
            self.game.screen.blit(self.image,self.rect)


