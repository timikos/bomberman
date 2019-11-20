import pygame

from objects.base import DrawObject

class Door(DrawObject):
    filename = 'images/door/door.png'

    def __init__(self, game, hidden=True, x=40, y=80):
        super().__init__(game)
        self.image = pygame.image.load(Door.filename)
        self.hidden = hidden
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 35)


    def collides_with(self, bomberman):
        """Персонаж должен зайти в дверь для завершения уровня"""
        return self.rect.colliderect(bomberman)


    def show_door(self):
        self.hidden = False
        self.rect.x = 45

    def process_logic(self):
        pass

    def process_draw(self):
        """Метод появления двери. Дверь появляется при условии, что все призраки убиты."""
        # Дверь не должна появляться на месте неразрушаемых блоков
        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)
