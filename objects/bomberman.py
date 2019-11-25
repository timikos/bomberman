import pygame
from objects.base import DrawObject
from constants import BombermanProperties, ScreenProperties, FieldProperties
from Global import Globals

class Bomberman(DrawObject):
    filename = 'images/bomberman/bomberman.png'

    def __init__(self, game, x=BombermanProperties.RESPAWN_X, y=BombermanProperties.RESPAWN_Y, speed=1):
        super().__init__(game)
        self.image = pygame.image.load(Bomberman.filename)
        self.current_shift_x = BombermanProperties.DIRECTION_X
        self.current_shift_y = BombermanProperties.DIRECTION_Y
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, BombermanProperties.WIDTH, BombermanProperties.HEIGHT)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN :
            if chr(event.key) == 'w':
                self.image = pygame.image.load('images/bomberman/bomberman_up1.png')
                self.current_shift_y = -1
                self.current_shift_x = 0
                Globals.TurnLeft = False
                Globals.TurnRight = False
            elif chr(event.key) == 's':
                self.image = pygame.image.load('images/bomberman/bomberman_down1.png')
                self.current_shift_y = 1
                self.current_shift_x = 0
                Globals.TurnLeft = False
                Globals.TurnRight = False
            elif chr(event.key) == 'a':
                self.image = pygame.image.load('images/bomberman/bomberman_left1.png')
                self.current_shift_y = 0
                self.current_shift_x = -1
                Globals.IsOnMove = True
                Globals.TurnLeft = True
            elif chr(event.key) == 'd':
                self.image = pygame.image.load('images/bomberman/bomberman_right1.png')
                self.current_shift_y = 0
                self.current_shift_x = 1
                Globals.IsOnMove = True
                Globals.TurnRight = True
            elif event.key == pygame.K_SPACE:
                cur_cell = self.game.scenes[1].field.get_cell_by_pos(self.rect.x, self.rect.y)
                self.game.scenes[1].bomb.create_bomb(cur_cell[0], cur_cell[1])
                Globals.TurnLeft = False
                Globals.TurnRight = False

        elif event.type == pygame.KEYUP:
            if event.key in [97, 100, 115, 119]:
                self.current_shift_x = 0
                self.current_shift_y = 0
                self.image = pygame.image.load('images/bomberman/bomberman.png')
                Globals.IsOnMove = False
                Globals.TurnLeft = False
                Globals.TurnRight = False

    def process_logic(self):
        if self.current_shift_y == 1:
            if self.rect.y <= self.game.height - ScreenProperties.SCREEN_BORDER_HEIGHT:
                self.rect.y += self.speed
        elif self.current_shift_y == -1:
            if self.rect.y > FieldProperties.CELL_LENGTH:
                self.rect.y -= self.speed
        elif self.current_shift_x == 1:
            if self.rect.x <= self.game.width - ScreenProperties.SCREEN_BORDER_WIDTH+10000:
                Globals.FieldPosition += self.speed
        elif self.current_shift_x == -1:
            if self.rect.x > FieldProperties.CELL_LENGTH * 2:
                Globals.FieldPosition -= self.speed


    def collides_with(self, other):
        return self.rect.colliderect(other)


    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
