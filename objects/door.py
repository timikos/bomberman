import pygame

from objects.base import DrawObject


class Door(DrawObject):
    filename = 'images/door/door.png'

    def __init__(self, game, x=100, y=100):
        super().__init__(game)
        self.image = pygame.image.load(Door.filename)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()  # rect необходим для коллизии игрока с дверью

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def show_door(self):
        """Метод появления двери. Дверь появляется при условии, что все призраки убиты."""
        pass

    def collides_with(self, bomberman):
        """Персонаж должен зайти в дверь для завершения уровня"""
        pass

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
