"""
Классы Block, IndestructibleBlock, IndestructibleBlockMap, DestroyedBlock, DestroyableBlockMap

Описание: данные классы реализуют заполнение поля блоками различных видов
"""
import pygame
from random import randint
from constants import FieldProperties
from objects.base import DrawObject
from Global import Globals

class Block(DrawObject):
    """Базовый класс блоков"""
    def __init__(self, game, x=0, y=0, cell_length=FieldProperties.CELL_LENGTH):
        super().__init__(game)
        self.border = []
        self.x = x * cell_length
        self.y = y * cell_length
        self.cell_length = cell_length
        self.rect = pygame.Rect(self.x, self.y, cell_length, 35)


class IndestructibleBlock(Block):
    """Неразрушаемый блок"""
    filename = 'images/blocks/block.png'

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.x = x * self.cell_length
        self.y = y * self.cell_length
        self.image = pygame.image.load(IndestructibleBlock.filename)

    def update_x(self, x):
        """Обновление позиции"""
        self.rect.x = self.x - x

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def process_event(self, event):
        pass

    def collides_with(self, other):
        """Коллизия с объектами"""
        return self.rect.colliderect(other)


class IndestructibleBlockMap(DrawObject):
    """Сетка неразрушаемых блоков"""
    def __init__(self, game, x=0, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.game = game
        self.x = x
        self.y = y
        self.tiles = []
        self.width = width
        self.height = height
        self.make_tilemap(game, width, height)

    def make_tilemap(self, game, width, height):
        """Создание сетки с блокми"""
        for x in range(width):
            self.tiles += [[]]  # Двумерный массив с блоками
            for y in range(height):
                if (x == 0 or x == width - 1 or y == 0 or y == height - 1) \
                        or ((x + 1) % 2 != 0 and (y + 1) % 2 != 0):
                    self.tiles[-1].append(IndestructibleBlock(game, self.x + x + 1, self.y + y))

    def process_draw(self):
        for x in self.tiles:
            for tile in x:
                tile.update_x(Globals.FieldPosition - 400)
                tile.process_draw()

    def process_event(self, event):
        for x in self.tiles:
            for tile in x:
                tile.process_event(event)


class DestroyedBlock(Block):
    """Разрушаемый блок"""
    """Список картинок состояния"""
    images = ['images/blocks/d_block_0.png',
              'images/blocks/d_block_1.png',
              'images/blocks/d_block_2.png',
              'images/blocks/d_block_3.png',
              'images/blocks/d_block_4.png',
              'images/blocks/d_block_5.png',
              'images/blocks/d_block_6.png']

    explosion_event = pygame.USEREVENT + 1

    def __init__(self, game, x=0, y=0):
        super().__init__(game, x, y)
        self.x = x * self.cell_length
        self.y = y * self.cell_length
        self.destruction_time = 5
        self.readyToBreak = False
        self.isDestroyed = False
        self.image = pygame.image.load(DestroyedBlock.images[0])
        self.start_ticks = 0

    def destruction(self):
        """Анимация разрушения блока"""
        mil_sec = (pygame.time.get_ticks() - self.start_ticks) // (self.destruction_time * 20) + 1
        self.image = pygame.image.load(DestroyedBlock.images[mil_sec])
        self.game.screen.blit(self.image, self.rect)
        return mil_sec

    def process_draw(self):
        self.update_x(Globals.FieldPosition - 400)
        if not self.isDestroyed:
            self.game.screen.blit(self.image, self.rect)
            if self.readyToBreak:
                if self.destruction() >= self.destruction_time:
                    self.isDestroyed = True

    def process_event(self, event):
        pass

    def update_x(self, x):
        """Обновление позиции"""
        self.rect.x = self.x - x

    def collides_with(self, other):
        """Коллизия с объектом"""
        if not self.isDestroyed:
            return self.rect.colliderect(other)
        else:
            return False


class DestroyedBlockMap(DrawObject):
    """Сетка разрушаемых блоков"""
    def __init__(self, game, x=0, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.x = x
        self.y = y
        self.tiles = []
        for x in range(width):
            self.tiles += [[]]  # Двумерный массив блоков
            for y in range(height):
                if not (x == 0 or x == width - 1 or y == 0 or y == height - 1) \
                        and not ((x + 1) % 2 != 0 and (y + 1) % 2 != 0) and (randint(0, 170) // 100):
                    self.tiles[-1].append(DestroyedBlock(game, self.x + x + 1, self.y + y))

    def process_draw(self):
        for x in self.tiles:
            for tile in x:
                tile.process_draw()

    def process_event(self, event):
        for x in self.tiles:
            for tile in x:
                tile.process_event(event)

    def get_ready_to_break_blocks(self):
        arr = []
        for x in self.tiles:
            for tile in x:
                if tile.readyToBreak is True and tile.isDestroyed is False:
                    arr.append(tile.rect)
        return arr
