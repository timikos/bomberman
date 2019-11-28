"""
Классы BombFire, Bomb, BombList

Описание: данные классы реализуют создание бомбы и её взрыв
"""

import pygame
from objects.base import DrawObject
from constants import BombProperties, FieldProperties
from Global import Globals
from objects.music import Sound


class BombFire:
    fire_filename = 'images/bombs/fire_center.png'

    def __init__(self, game, update_power=1):
        self.game = game
        self.fire_image = pygame.image.load(BombFire.fire_filename)
        self.count_fire_sides = 4
        self.update_power = update_power  # На сколько клеток расширим базовый огонь
        self.fire_rects = []

    def create_fire(self, x, y):
        """Создание огня"""
        self.delete_fire()
        for i in range(self.update_power):
            self.fire_rects.append(
                pygame.Rect(x - FieldProperties.CELL_LENGTH * (i + 1), y, BombProperties.WIDTH, BombProperties.HEIGHT))
            self.fire_rects.append(
                pygame.Rect(x + FieldProperties.CELL_LENGTH * (i + 1), y, BombProperties.WIDTH, BombProperties.HEIGHT))
            self.fire_rects.append(
                pygame.Rect(x, y - FieldProperties.CELL_LENGTH * (i + 1), BombProperties.WIDTH, BombProperties.HEIGHT))
            self.fire_rects.append(
                pygame.Rect(x, y + FieldProperties.CELL_LENGTH * (i + 1), BombProperties.WIDTH, BombProperties.HEIGHT))
        self.fire_rects.append(pygame.Rect(x, y, BombProperties.WIDTH, BombProperties.HEIGHT))  # Центральный огонь

    def show_fire(self):
        """Отрисовка огня"""
        for fire_rect in self.fire_rects:
            self.game.screen.blit(self.fire_image, fire_rect)

    def delete_fire(self):
        """Удаление огня"""
        self.fire_rects.clear()


class Bomb(DrawObject):
    filename = 'images/bombs/bomb.png'

    def __init__(self, game, x, y, bomb_power, hidden=True):
        super().__init__(game)
        self.hidden = hidden
        self.start_ticks = 0
        self.bomb_power = bomb_power
        self.bomb_fire = BombFire(self.game, self.bomb_power)
        self.image = pygame.image.load(Bomb.filename)
        self.rect = pygame.Rect(0, 0, FieldProperties.CELL_LENGTH, FieldProperties.CELL_LENGTH)
        self.x = 0
        self.destroy = False
        self.create_bomb(x, y)

    def create_bomb(self, x, y):
        """Создание бомбы"""
        self.x = x
        self.rect.x = x + 3
        self.rect.y = y + 3
        self.hidden = False
        self.start_ticks = pygame.time.get_ticks()

    def hide_bomb(self):
        """Скрытие бомбы"""
        self.hidden = True
        self.start_ticks = 0
        self.destroy = True

    def process_draw(self):
        self.update_x(Globals.FieldPosition)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if not self.hidden and seconds <= 2:
            self.game.screen.blit(self.image, self.rect)
        elif not self.hidden and 2 < seconds <= 3:
            self.bomb_fire.create_fire(self.rect.x, self.rect.y)
            self.bomb_fire.show_fire()
            Sound.explosion.play(0)
        elif not self.hidden and seconds > 3:
            self.bomb_fire.delete_fire()
            self.hide_bomb()

    def collides_with(self, other):
        """Коллизия с объектами"""
        return self.rect.colliderect(other)

    def update_x(self, x):
        """Обновление позиции"""
        self.rect.x = self.x - x


class BombsList(DrawObject):
    def __init__(self, game):
        super().__init__(game)
        self.bombs = []

    def add_bomb(self, x, y, bomb_power=1):
        """Добавление бомбы в список"""
        self.bombs.append(Bomb(self.game, x, y, bomb_power))

    def process_draw(self):
        for bomb in self.bombs:
            bomb.process_draw()
            if bomb.destroy:
                self.bombs.remove(bomb)
