"""
Классы Ghost, SpeedGhost, SuperGhost

Описание: данные классы реализуют врагов разнличных видов
"""

import pygame
from random import randint
from objects.base import DrawObject
from constants import EnemyProperties
from Global import Globals


class Ghost(DrawObject):
    """Обычный монстр"""
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
        self.glob = Globals.FieldPosition
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
        if Globals.TurnRight:
            self.rect.x -= (Globals.FieldPosition - self.glob)
            self.glob = Globals.FieldPosition
        if Globals.TurnLeft:
            self.rect.x += (self.glob - Globals.FieldPosition)
            self.glob = Globals.FieldPosition

        # Движение по горизонтали:
        if self.current_shift_x:
            # Движение вправо
            if self.current_shift_x == 1:
                self.image = self.images[1]
                self.rect.x += self.speed
            # Движение влево
            elif self.current_shift_x == -1:
                self.rect.x -= self.speed
                self.image = self.images[2]
        # Движение по вертикали:
        elif self.current_shift_y:
            # Движение вниз
            if self.current_shift_y == 1:
                self.image = self.images[0]
                self.rect.y += self.speed
            # Движение вверх
            elif self.current_shift_y == -1:
                self.image = self.images[0]
                self.rect.y -= self.speed
                
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

    def change_move_after_collision(self):
        """Изменение направления движения после коллизии с блоком"""
        # Движение по горизонтали
        if self.current_shift_x:
            self.current_shift_y = randint(-1, 1)
            # Измененяем напралвление движения с горизонтального на вертикальное
            if self.current_shift_y:
                self.rect.x -= self.current_shift_x*5
                self.current_shift_x = 0
            # Либо на противоположное
            elif self.current_shift_y == 0:
                self.current_shift_x *= -1
        # Движение по вертикали
        else:
            if self.current_shift_y:
                self.current_shift_x = randint(-1, 1)
                # Измененяем напралвление движения с вертикального на горизонтальное
                if self.current_shift_x:
                    self.rect.y -= self.current_shift_y*5
                    self.current_shift_y = 0
                # Либо на противоположное
                elif self.current_shift_x == 0:
                    self.current_shift_y *= -1


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


class SpeedGhost(Ghost):
    """Монстр с увеличенной скоростью"""
    filename = 'images/ghosts/enemy_2_Main.png'

    """Список изображений состояния"""
    img_filenames = ['images/ghosts/enemy_2_Main.png',
                     'images/ghosts/enemy_2_Right.png',
                     'images/ghosts/enemy_2_Left.png']
    images = None

    def __init__(self, game, speed=2, x=0, y=0):
        super().__init__(game, speed, x=x, y=y)

        """Загрузка картинок в список"""
        if SpeedGhost.images is None:
            SpeedGhost.images = []
            for name in SpeedGhost.img_filenames:
                SpeedGhost.images.append(pygame.image.load(name))


class SuperGhost(Ghost):
    """Монстр с увеличенной скоростью и возможностью передвигаться через разрушаемые блоки"""
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

        self.pass_throw_destruct_blocks = True  # Возможность передвигаться сквозь блоки
