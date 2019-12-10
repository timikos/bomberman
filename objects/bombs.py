"""
Классы BombFire, Bomb, BombList

Описание: данные классы реализуют создание бомбы и её взрыв
"""

import pygame
from objects.base import DrawObject
from constants import BombProperties, FieldProperties
from Global import Globals
from objects.music import Sound


class Fire(DrawObject):
    fire_center = 'images/bombs/fire_center.png'
    fire_horizontal = 'images/bombs/fire_horizontal.png'
    fire_vertical = 'images/bombs/fire_vertical.png'
    fire_left = 'images/bombs/fire_left.png'
    fire_right = 'images/bombs/fire_right.png'
    fire_up = 'images/bombs/fire_up.png'
    fire_down = 'images/bombs/fire_down.png'

    def __init__(self, game, x, y, side):
        super().__init__(game)
        if side == 'left' or side == 'right':
            self.fire_image = pygame.image.load(Fire.fire_horizontal)
        elif side == 'up' or side == 'down':
            self.fire_image = pygame.image.load(Fire.fire_vertical)
        elif side == 'end_left':
            self.fire_image = pygame.image.load(Fire.fire_left)
        elif side == 'end_right':
            self.fire_image = pygame.image.load(Fire.fire_right)
        elif side == 'end_up':
            self.fire_image = pygame.image.load(Fire.fire_up)
        elif side == 'end_down':
            self.fire_image = pygame.image.load(Fire.fire_down)
        elif side == 'center':
            self.fire_image = pygame.image.load(Fire.fire_center)
        self.fire_rect = pygame.Rect(x, y, BombProperties.WIDTH, BombProperties.HEIGHT)
        self.active = False
        self.x = x

    def process_draw(self):
        self.update_x(Globals.FieldPosition)
        self.game.screen.blit(self.fire_image, self.fire_rect)

    def update_x(self, x):
        """Обновление позиции"""
        self.fire_rect.x = self.x - x


class BombFire(DrawObject):

    def __init__(self, game, x, y, update_power=1):
        super().__init__(game)
        self.game = game
        self.count_fire_sides = 4
        self.update_power = update_power  # На сколько клеток расширим базовый огонь
        self.fire_rects = []
        self.left = True
        self.right = True
        self.up = True
        self.down = True
        self.create_fire(x, y)

    def create_fire(self, x, y):
        for i in range(self.update_power):
            left_x_fire = x - FieldProperties.CELL_LENGTH * (i + 1)
            right_x_fire = x + FieldProperties.CELL_LENGTH * (i + 1)
            up_y_fire = y - FieldProperties.CELL_LENGTH * (i + 1)
            down_y_fire = y + FieldProperties.CELL_LENGTH * (i + 1)
            if self.left:
                fire_side = 'left'
                if i + 1 >= self.update_power:
                    fire_side = 'end_left'
                lfire = Fire(self.game, left_x_fire, y, fire_side)
                for tiles in self.game.scenes[1].tilemap.tiles:
                    for block in tiles:
                        lfire.update_x(Globals.FieldPosition)
                        if block.collides_with(lfire.fire_rect):
                            self.left = False
                            break
                else:
                    for block in self.game.scenes[1].blocks:
                        lfire.update_x(Globals.FieldPosition)
                        if block.collides_with(lfire.fire_rect):
                            self.fire_rects.append(lfire)
                            self.left = False
                            break
                    else:
                        self.fire_rects.append(lfire)
            if self.right:
                fire_side = 'right'
                if i + 1 >= self.update_power:
                    fire_side = 'end_right'
                rfire = Fire(self.game, right_x_fire, y, fire_side)
                for tiles in self.game.scenes[1].tilemap.tiles:
                    for block in tiles:
                        rfire.update_x(Globals.FieldPosition)
                        if block.collides_with(rfire.fire_rect):
                            self.right = False
                            break
                else:
                    for block in self.game.scenes[1].blocks:
                        rfire.update_x(Globals.FieldPosition)
                        if block.collides_with(rfire.fire_rect):
                            self.fire_rects.append(rfire)
                            self.right = False
                            break
                    else:
                        self.fire_rects.append(rfire)
            if self.up:
                fire_side = 'up'
                if i + 1 >= self.update_power:
                    fire_side = 'end_up'
                upfire = Fire(self.game, x, up_y_fire, fire_side)
                for tiles in self.game.scenes[1].tilemap.tiles:
                    for block in tiles:
                        upfire.update_x(Globals.FieldPosition)
                        if block.collides_with(upfire.fire_rect):
                            self.up = False
                            break
                else:
                    for block in self.game.scenes[1].blocks:
                        upfire.update_x(Globals.FieldPosition)
                        if block.collides_with(upfire.fire_rect):
                            self.fire_rects.append(upfire)
                            self.up = False
                            break
                    else:
                        self.fire_rects.append(upfire)
            if self.down:
                fire_side = 'down'
                if i + 1 >= self.update_power:
                    fire_side = 'end_down'
                dfire = Fire(self.game, x, down_y_fire, fire_side)
                for tile_row in self.game.scenes[1].tilemap.tiles:
                    for tile in tile_row:
                        dfire.update_x(Globals.FieldPosition)
                        if tile.collides_with(dfire.fire_rect):
                            self.down = False
                            break
                else:
                    for block in self.game.scenes[1].blocks:
                        dfire.update_x(Globals.FieldPosition)
                        if block.collides_with(dfire.fire_rect):
                            self.fire_rects.append(dfire)
                            self.down = False
                            break
                    else:
                        self.fire_rects.append(dfire)
        self.fire_rects.append(Fire(self.game, x, y, 'center'))  # Центральный огонь

    def delete_fire(self):
        """Удаление огня"""
        self.fire_rects.clear()

    def activated(self):
        for fire in self.fire_rects:
            fire.active = True

    def process_draw(self):
        """Отрисовка огня"""
        for fire in self.fire_rects:
            fire.process_draw()


class Bomb(DrawObject):
    filename = 'images/bombs/bomb.png'

    def __init__(self, game, x, y, bomb_power, hidden=True):
        super().__init__(game)
        self.hidden = hidden
        self.start_ticks = 0
        self.bomb_power = bomb_power
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
        self.bomb_fire = BombFire(self.game, x, y, self.bomb_power)
        self.start_ticks = pygame.time.get_ticks()

    def hide_bomb(self):
        """Скрытие бомбы"""
        self.bomb_fire.delete_fire()
        self.hidden = True
        self.start_ticks = 0
        self.destroy = True

    def process_draw(self):
        self.update_x(Globals.FieldPosition)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if not self.hidden and seconds <= 2:
            self.game.screen.blit(self.image, self.rect)
        elif not self.hidden and 2 < seconds <= 3:
            self.bomb_fire.activated()
            self.bomb_fire.process_draw()
            # Sound.explosion.play(0)
        elif not self.hidden and seconds > 3:
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
                Globals.UpdateNext = True
