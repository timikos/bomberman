"""
Классы Ghost, SpeedGhost, SuperGhost

Описание: данные классы реализуют врагов разнличных видов
"""

import pygame
from random import randint, randrange
from objects.base import DrawObject
from constants import EnemyProperties,ScreenProperties,FieldProperties
from Global import Globals



class Ghost(DrawObject):
    filename = 'images/ghosts/enemy_1_Main.png'

    """Список картинок состояния"""
    img_filenames = [
        'images/ghosts/enemy_1_Main.png',
        'images/ghosts/enemy_1_Right.png',
        'images/ghosts/enemy_1_Left.png'
    ]
    images = None

    def __init__(self, game, speed=1, hidden=False, x=40, y=40):
        super().__init__(game)
        self.image = pygame.image.load(self.filename)

        """Загрузка картинок в список"""
        if Ghost.images is None:
            Ghost.images = []
            for name in Ghost.img_filenames:
                Ghost.images.append(pygame.image.load(name))

        self.hidden = hidden
        self.pass_throw_destruct_blocks = False  # Возможность передвигаться сквозь блоки
        self.x = x
        self.y = y
        self.glob=Globals.FieldPosition
        self.current_shift_x = EnemyProperties.DIRECTION_X
        self.current_shift_y = EnemyProperties.DIRECTION_Y
        self.speed = speed
        self.window_width = self.game.width
        self.window_height = self.game.height
        self.rect = pygame.Rect(self.x, self.y, EnemyProperties.WIDTH, EnemyProperties.HEIGHT)
        self.rect.x = self.x
        self.rect.y = self.y
        self.start_move()
        self.data = self.images

    def process_event(self, event):
        pass


    def process_logic(self):
        """Логика движения призраков"""
        # Движение вниз и проверка границ
        if self.current_shift_y == 1 and self.rect.y < self.game.height - ScreenProperties.SCREEN_BORDER_HEIGHT:
            self.image = self.images[0]
            self.rect.y += self.speed
        # Движение вверх и проверка границ
        elif self.current_shift_y == -1 and self.rect.y > 40:
            self.image = self.images[0]
            self.rect.y -= self.speed
        # Движение вправо и проверка границ
        elif self.current_shift_x == 1 and self.rect.x < self.game.width - ScreenProperties.SCREEN_BORDER_WIDTH:
            self.image = self.images[1]
            self.rect.x += self.speed
        # Движение влево и проверка границ
        elif self.current_shift_x == -1 and self.rect.x > 80:
            self.rect.x -= self.speed
            self.image = self.images[2]
            self.rect.x -= 1
        if Globals.TurnRight:
            self.rect.x -= (Globals.FieldPosition-self.glob)
            self.glob = Globals.FieldPosition
        if Globals.TurnLeft:
            self.rect.x += (self.glob-Globals.FieldPosition)
            self.glob = Globals.FieldPosition
        if self.rect.x == FieldProperties.CELL_LENGTH * 2 or self.rect.y == FieldProperties.CELL_LENGTH or\
                self.rect.y == self.game.height - ScreenProperties.HEIGHT or \
                self.rect.x == self.game.width - ScreenProperties.WIDTH:
            if self.rect.x == FieldProperties.CELL_LENGTH * 2:
                self.rect.x += self.speed
            if self.rect.x == self.game.width - ScreenProperties.SCREEN_BORDER_WIDTH:
                self.rect.x -= self.speed
            if self.rect.y == FieldProperties.CELL_LENGTH:
                self.rect.y += self.speed
            if self.rect.y == self.game.height - ScreenProperties.HEIGHT:
                self.rect.y -= self.speed
            self.start_move()

    def start_move(self):
        """Начало движения"""
        direction_move = randint(0, 3)
        if direction_move == 0:
            self.current_shift_x = -1
        elif direction_move == 1:
            self.current_shift_x = 1
        elif direction_move == 2:
            self.current_shift_y = 1
        elif direction_move == 3:
            self.current_shift_y = -1

    def collides_with(self, other):
        """Коллизия с объектами"""
        return self.rect.colliderect(other)

    def process_draw(self):
        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)
        if self.hidden:
            self.rect.x = 0
            self.rect.y = 0
            self.current_shift_x = 0
            self.current_shift_y = 0


"""Монстр с увеличенной скоростью"""
class SpeedGhost(Ghost):
    filename = 'images/ghosts/enemy_2_Main.png'

    """Список изображений состояния"""
    img_filenames = ['images/ghosts/enemy_2_Main.png',
                     'images/ghosts/enemy_2_Right.png',
                     'images/ghosts/enemy_2_Left.png']
    images = None

    def __init__(self, game, speed=2, x=0, y=0):
        super().__init__(game, speed, x=x, y=y)
        self.image = pygame.image.load(SpeedGhost.filename)

        """Загрузка картинок в список"""
        if SpeedGhost.images is None:
            SpeedGhost.images = []
            for name in SpeedGhost.img_filenames:
                SpeedGhost.images.append(pygame.image.load(name))


"""Монстр с увеличенной скоростью и возможностью передвигаться через разрушаемые блоки"""
class SuperGhost(Ghost):
    filename = 'images/ghosts/enemy_3_Main.png'

    """Список изображений состояния"""
    img_filenames = ['images/ghosts/enemy_3_Main.png',
                     'images/ghosts/enemy_3_Right.png',
                     'images/ghosts/enemy_3_Left.png']
    images = None

    def __init__(self, game, speed=2, x=0, y=0):
        super().__init__(game, speed, x=x, y=y)

        """Загрузка картинок в список"""
        if SuperGhost.images is None:
            SuperGhost.images = []
            for name in SuperGhost.img_filenames:
                SuperGhost.images.append(pygame.image.load(name))

        self.pass_throw_destruct_blocks = True # Возможность передвигаться сквозь блоки

