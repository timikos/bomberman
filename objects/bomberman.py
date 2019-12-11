"""
Класс Bomberman

Описание: данный класс реализует создание главного героя и его логику
"""

import pygame
from objects.base import DrawObject
from constants import BombermanProperties, ScreenProperties, FieldProperties
from Global import Globals


class Bomberman(DrawObject):
    filename = 'images/bomberman/bomberman.png'

    """Список картинок состояния"""
    img_filenames = [
        'images/bomberman/bomberman.png',
        'images/bomberman/bomberman_up1.png',
        'images/bomberman/bomberman_down1.png',
        'images/bomberman/bomberman_left1.png',
        'images/bomberman/bomberman_right1.png',
        'images/bomberman/bomberman_died.png',
    ]
    images = None

    def __init__(self, game, x=BombermanProperties.RESPAWN_X, y=BombermanProperties.RESPAWN_Y, speed=1):
        super().__init__(game)
        self.image = pygame.image.load(Bomberman.filename)

        if Bomberman.images is None:
            Bomberman.images = []
            for name in Bomberman.img_filenames:
                Bomberman.images.append(pygame.image.load(name))

        self.current_shift_x = BombermanProperties.DIRECTION_X
        self.current_shift_y = BombermanProperties.DIRECTION_Y
        self.x = x
        self.y = y
        self.speed = speed
        self.bomb_power = 1
        self.multi_bomb = False
        self.rect = pygame.Rect(self.x, self.y, BombermanProperties.WIDTH, BombermanProperties.HEIGHT)
        self.start_ticks = 0

    def process_event(self, event):
        """События нажатия кнопок"""
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == 'w':
                self.image = Bomberman.images[1]
                self.current_shift_y = -1
                self.current_shift_x = 0
                Globals.TurnLeft = False
                Globals.TurnRight = False
            elif chr(event.key) == 's':
                self.image = Bomberman.images[2]
                self.current_shift_y = 1
                self.current_shift_x = 0
                Globals.TurnLeft = False
                Globals.TurnRight = False
            elif chr(event.key) == 'a':
                self.image = Bomberman.images[3]
                self.current_shift_y = 0
                self.current_shift_x = -1
                Globals.TurnLeft = True
            elif chr(event.key) == 'd':
                self.image = Bomberman.images[4]
                self.current_shift_y = 0
                self.current_shift_x = 1
                Globals.TurnRight = True
            elif event.key == pygame.K_SPACE:
                cur_cell = self.game.scenes[1].field.get_cell_by_pos(self.rect.centerx, self.rect.centery)
                if len(self.game.scenes[1].bomb_list.bombs) == 0 or self.multi_bomb:
                    self.game.scenes[1].bomb_list.add_bomb(cur_cell[0], cur_cell[1], self.bomb_power)
                Globals.TurnLeft = False
                Globals.TurnRight = False

        elif event.type == pygame.KEYUP:
            """Проверка на отжатие кнопок"""
            if event.key in [97, 100, 115, 119]:
                self.current_shift_x = 0
                self.current_shift_y = 0
                self.image = Bomberman.images[0]
                Globals.TurnLeft = False
                Globals.TurnRight = False

    def process_logic(self):
        """Логика бомбермена"""
        if self.current_shift_y == 1:
            if self.rect.y <= self.game.height - ScreenProperties.SCREEN_BORDER_HEIGHT:
                self.rect.y += self.speed
        elif self.current_shift_y == -1:
            if self.rect.y > FieldProperties.CELL_LENGTH:
                self.rect.y -= self.speed
        elif self.current_shift_x == 1:
            if self.rect.x <= self.game.width - ScreenProperties.SCREEN_BORDER_WIDTH + 10000:
                if self.rect.x <= 600:
                    self.rect.x += self.speed
                    Globals.UpdateDisplay = False
                else:
                    Globals.FieldPosition += self.speed
                    Globals.UpdateDisplay = True
        elif self.current_shift_x == -1:
            if self.rect.x > FieldProperties.CELL_LENGTH * 2:
                if self.rect.x >= 200:
                    self.rect.x -= self.speed
                    Globals.UpdateDisplay = False
                else:
                    Globals.FieldPosition -= self.speed
                    Globals.UpdateDisplay = True
        else:
            Globals.UpdateDisplay = False
        if Globals.FieldPosition < 285:
            Globals.FieldPosition = 285
        if Globals.FieldPosition > 995:
            Globals.FieldPosition = 995

    def collides_with(self, other):
        """Коллизия с объектом"""
        return self.rect.colliderect(other)

    # def collides_with_list(self,list):
    """Коллизия со списком объектов"""

    # print(self.rect.collidelist(list))
    # return self.rect.collidelist(list)

    def is_invulnerable(self):
        """Проверяет, неуязвим ли персонаж"""
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if seconds <= 3:
            self.image = Bomberman.images[5]
            return True
        return False

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
