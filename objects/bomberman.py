import pygame
import time
from objects.base import DrawObject

class Bomberman(DrawObject):
    filename = 'images/bomberman/bomberman.png'

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
                self.image = pygame.image.load('images/bomberman/bomberman_up1.png')
                # self.image = pygame.image.load('images/bomberman/bomberman_up2.png')
                self.current_shift_y = -1
            elif chr(event.key) == 's':
                self.image = pygame.image.load('images/bomberman/bomberman_down1.png')
                self.current_shift_y = 1
            elif chr(event.key) == 'a':
                self.image = pygame.image.load('images/bomberman/bomberman_left1.png')
                self.current_shift_x = -1
            elif chr(event.key) == 'd':
                self.image = pygame.image.load('images/bomberman/bomberman_right1.png')
                self.current_shift_x = 1
        elif event.type == pygame.KEYUP:
            if event.key in [97, 100, 115, 119]:
                self.current_shift_x = 0
                self.current_shift_y = 0
                self.image = pygame.image.load('images/bomberman/bomberman.png')

    def process_logic(self):

        if self.current_shift_y == 1:
            if self.rect.y <= self.game.height - 80:
                self.rect.y += 2
        elif self.current_shift_y == -1:
            if self.rect.y > 40:
                self.rect.y -= 2
        elif self.current_shift_x == 1:
            if self.rect.x <= self.game.width - 80:
                self.rect.x += 2
        elif self.current_shift_x == -1:
            if self.rect.x > 40:
                self.rect.x -= 2


    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
