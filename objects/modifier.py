import pygame
from objects.base import DrawObject


class SpeedModifier(DrawObject):
    filename = 'images/modifiers/speed.png'

    def __init__(self, game, x=0, y=0, hidden=False):
        super().__init__(game)
        self.image = pygame.image.load(SpeedModifier.filename)
        self.x = x
        self.y = y
        self.hidden = hidden
        self.rect = pygame.Rect(self.x, self.y, 30, 35)

    def hide(self):
        self.hidden = True
        self.rect.x = 0
        self.rect.y = 0

    def collides_with(self, bomberman):
        return self.rect.colliderect(bomberman)

    def process_draw(self):
        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)
