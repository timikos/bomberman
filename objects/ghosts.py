import pygame
from random import randint

from objects.base import DrawObject

class Ghost(DrawObject):
    filename = 'images/ghosts/ghostE.png'

    def __init__(self, game, x = 40, y = 40):
        super().__init__(game)
        self.image = pygame.image.load(Ghost.filename)
        self.x = x
        self.y = y
        self.current_shift_x = 0
        self.current_shift_y = 0
        self.window_width = self.game.width
        self.window_height = self.game.height
        self.rect = pygame.Rect(self.x, self.y, 30, 35)
        self.rect.x = randint(40, self.window_width - self.rect.width - 200)
        self.rect.y = randint(40, self.window_height - self.rect.height - 200)
        self.direction = None
        self.start_move()

    def process_event(self, event):
        pass

    def process_logic(self):
        if self.current_shift_y == 1:
            self.image = pygame.image.load('images/ghosts/ghostEdown.png')
            self.rect.y += 1
        elif self.current_shift_y == -1:
            self.image = pygame.image.load('images/ghosts/ghostEup.png')
            self.rect.y -= 1
        elif self.current_shift_x == 1:
            self.image = pygame.image.load('images/ghosts/ghostEright.png')
            self.rect.x += 1
        elif self.current_shift_x == -1:
            self.image = pygame.image.load('images/ghosts/ghostEleft.png')
            self.rect.x -= 1
        if self.rect.x == 80 or self.rect.y == 40 or self.rect.y == self.game.height - 150 or self.rect.x == self.game.width - 160:
            self.current_shift_y = 0
            self.current_shift_x = 0
            self.image = pygame.image.load('images/ghosts/ghostE.png')
            self.start_move()


    def start_move(self):
        start_move = randint(0, 3)
        if start_move == 0 and self.rect.x != 40 and self.direction != start_move:
            self.current_shift_x = -1
            self.direction = start_move
        elif start_move == 1 and self.rect.y != self.game.height - 150 and self.direction != start_move:
            self.current_shift_y = 1
            self.direction = start_move
        elif start_move == 2 and self.rect.x != self.game.width - 80 and self.direction != start_move:
            self.current_shift_x = 1
            self.direction = start_move
        elif start_move == 3 and self.rect.y != 40 and self.direction != start_move:
            self.current_shift_y = -1
            self.direction = start_move

    def collides_with(self, bomberman):
        return self.rect.colliderect(bomberman)


    def collision(self, other_ball):
        # self.shift_x, other_ball.shift_x = other_ball.shift_x, self.shift_x
        # self.shift_y, other_ball.shift_y = other_ball.shift_y, self.shift_y
        pass


    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
