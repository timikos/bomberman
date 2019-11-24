import pygame
from random import randint, randrange
from objects.base import DrawObject
from constants import EnemyProperties,ScreenProperties,FieldProperties
from Global import Globals


class Ghost(DrawObject):
    filename = 'images/ghosts/enemy_1_Main.png'

    def __init__(self, game, hidden=False, x = 40, y = 40):
        super().__init__(game)
        self.image = pygame.image.load(Ghost.filename)
        self.hidden = hidden
        self.x = x
        self.y = y
        self.glob=Globals.FieldPosition
        self.current_shift_x = EnemyProperties.DIRECTION_X
        self.current_shift_y = EnemyProperties.DIRECTION_Y
        self.window_width = self.game.width
        self.window_height = self.game.height
        self.rect = pygame.Rect(self.x, self.y, EnemyProperties.WIDTH, EnemyProperties.HEIGHT)
        self.rect.x = randrange(80, self.window_width - self.rect.width - 200, 400)
        self.rect.y = randrange(40, self.window_height - self.rect.height - 200, 80)
        self.start_move()


    def process_event(self, event):
        pass

    def process_logic(self):
        if self.current_shift_y == 1 and self.rect.y < self.game.height - 150:
            self.image = pygame.image.load('images/ghosts/enemy_1_Main.png')
            self.rect.y += 1
        elif self.current_shift_y == -1 and self.rect.y > 40:
            self.image = pygame.image.load('images/ghosts/enemy_1_Main.png')
            self.rect.y -= 1
        elif self.current_shift_x == 1 and self.rect.x < self.game.width - 160:
            self.image = pygame.image.load('images/ghosts/enemy_1_Right.png')
            self.rect.x += 1
        elif self.current_shift_x == -1 and self.rect.x > 80:
            self.image = pygame.image.load('images/ghosts/enemy_1_Left.png')
            self.rect.x -= 1
        if Globals.TurnRight == True and self.glob != Globals.FieldPosition:
            self.rect.x -= 5
            self.glob = Globals.FieldPosition
        if Globals.TurnLeft == True and self.glob != Globals.FieldPosition:
            self.rect.x += 5
            self.glob = Globals.FieldPosition
        if self.rect.x == FieldProperties.CELL_LENGTH * 2 or self.rect.y == FieldProperties.CELL_LENGTH or\
                self.rect.y == self.game.height - ScreenProperties.HEIGHT or \
                self.rect.x == self.game.width - ScreenProperties.WIDTH:
            if self.rect.x == FieldProperties.CELL_LENGTH * 2:
                self.rect.x += 1
            if self.rect.x == self.game.width - ScreenProperties.SCREEN_BORDER_WIDTH:
                self.rect.x -= 1
            if self.rect.y == FieldProperties.CELL_LENGTH:
                self.rect.y += 1
            if self.rect.y == self.game.height - ScreenProperties.HEIGHT:
                self.rect.y -= 1
            self.start_move()


    def start_move(self):
        direction_move = randint(0, 3)
        if direction_move == 0 :
            self.current_shift_x = -1
        elif direction_move == 1 :
            self.current_shift_x = 1
        elif direction_move == 2 :
            self.current_shift_y = 1
        elif direction_move == 3:
            self.current_shift_y = -1

    def collides_with(self, other):
        return self.rect.colliderect(other)

    def process_draw(self):
        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)
        if self.hidden:
            self.rect.x = 0
            self.rect.y = 0
            self.current_shift_x = 0
            self.current_shift_y = 0
