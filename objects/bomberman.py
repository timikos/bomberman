import pygame
import time
from objects.base import DrawObject

class Bomberman(DrawObject):
    filename = 'images/bomberman.png'

    def __init__(self, game, x = 150, y = 150):
        super().__init__(game)
        self.image = pygame.image.load(Bomberman.filename)
        self.current_shift_x = 0
        self.current_shift_y = 0
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,150,150)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == 'w':
                self.image = pygame.image.load('images/bomberman_up1.jpg')
                self.image = pygame.image.load('images/bomberman_up2.jpg')
                self.current_shift_y = -1
            elif chr(event.key) == 's':
                self.image = pygame.image.load('images/bomberman_down1.jpg')
                self.current_shift_y = 1
            elif chr(event.key) == 'a':
                self.image = pygame.image.load('images/bomberman_left1.jpg')
                self.current_shift_x = -1
            elif chr(event.key) == 'd':
                self.image = pygame.image.load('images/bomberman_right1.jpg')
                self.current_shift_x = 1
        elif event.type == pygame.KEYUP:
            if event.key in [97, 100, 115, 119]:
                self.current_shift_x = 0
                self.current_shift_y = 0
                self.image = pygame.image.load('images/bomberman.jpg')

    def process_logic(self):

        if self.current_shift_y == 1:
            if self.rect.y <= self.game.height - 25:
                self.rect.y += 2
        elif self.current_shift_y == -1:
            if self.rect.y > 0:
                self.rect.y -= 2
        elif self.current_shift_x == 1:
            if self.rect.x <= self.game.width - 25:
                self.rect.x += 2
        elif self.current_shift_x == -1:
            if self.rect.x != 0:
                self.rect.x -= 2


    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)