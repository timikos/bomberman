"""
Классы Modifier, SpeedModifier, BombPowerModifier, AddLifeModifier

Описание: данные классы реализуют модификаторы различных видов
"""
import pygame
from objects.base import DrawObject
from Global import Globals
from objects.field import Field


class Modifier(DrawObject):
    """Базовый класс модификаторов"""
    def __init__(self, game, image, x=0, y=0, hidden=False):
        super().__init__(game)
        self.x, self.y = Field.get_cell_by_pos(x, y)
        self.hidden = hidden
        self.rect = pygame.Rect(self.x, self.y, 35, 35)
        self.image = image

    def hide(self):
        """Скрытие после коллизии"""
        self.hidden = True
        self.rect.x = 0
        self.rect.y = 0
        Globals.UpdateNext = True

    def collides_with(self, other):
        """Коллизия с объектами"""
        return self.rect.colliderect(other)

    def update_x(self, x):
        """Обновление позиции"""
        self.rect.x = self.x - x + 2
        self.rect.y = self.y + 2

    def process_draw(self):
        self.update_x(Globals.FieldPosition - 400)
        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)


"""Модификатор увеличения скорости"""


class SpeedModifier(Modifier):
    filename = 'images/modifiers/speed.png'
    name = 'speed'

    def __init__(self, game, x=0, y=0, hidden=False):
        self.image = pygame.image.load(SpeedModifier.filename)
        super().__init__(game, self.image, x, y, hidden)


"""Модификатор увеличения линии огня"""


class BombPowerModifier(Modifier):
    filename = 'images/modifiers/5.png'
    name = 'bomb_power'

    def __init__(self, game, x=0, y=0, hidden=False):
        self.image = pygame.image.load(BombPowerModifier.filename)
        super().__init__(game, self.image, x, y, hidden)


"""Модификатор увеличения жизней"""


class AddLifeModifier(Modifier):
    filename = 'images/modifiers/2.png'
    name = 'add_life'

    def __init__(self, game, x=0, y=0, hidden=False):
        self.image = pygame.image.load(AddLifeModifier.filename)
        super().__init__(game, self.image, x, y, hidden)


"""Модификатор увеличения количества бомб"""


class MultiBombModifier(Modifier):
    filename = 'images/modifiers/4.png'
    name = 'multi_bomb'

    def __init__(self, game, x=0, y=0, hidden=False):
        self.image = pygame.image.load(MultiBombModifier.filename)
        super().__init__(game, self.image, x, y, hidden)
