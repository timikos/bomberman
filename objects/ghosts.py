import pygame
from random import randint, randrange

from objects.base import DrawObject


class Ghost(DrawObject):
    filename = 'images/ghosts/ghostE.png'

    def __init__(self, game, x = 40, y = 40, x_bomber = 400, y_bomber = 300):
        super().__init__(game)
        self.image = pygame.image.load(Ghost.filename)
        self.x = x
        self.y = y
        self.x_bomber = x_bomber
        self.y_bomber = y_bomber
        self.bomber_rect = pygame.Rect(self.x_bomber,self.y_bomber,30,35)
        self.current_shift_x = 0
        self.current_shift_y = 0
        self.window_width = self.game.width
        self.window_height = self.game.height
        self.rect = pygame.Rect(self.x, self.y, 30, 35)
        self.rect.x = randrange(81, self.window_width - self.rect.width - 200, 80)
        self.rect.y = randrange(41, self.window_height - self.rect.height - 200, 80)
        self.start_move()

    def process_event(self, event):
        pass

    def process_logic(self):
        if self.current_shift_y == 1 and self.rect.y < self.game.height - 150:
            self.image = pygame.image.load('images/ghosts/ghostEdown.png')
            self.rect.y += 1
        elif self.current_shift_y == -1 and self.rect.y > 40:
            self.image = pygame.image.load('images/ghosts/ghostEup.png')
            self.rect.y -= 1
        elif self.current_shift_x == 1 and self.rect.x < self.game.width - 160:
            self.image = pygame.image.load('images/ghosts/ghostEright.png')
            self.rect.x += 1
        elif self.current_shift_x == -1 and self.rect.x > 80:
            self.image = pygame.image.load('images/ghosts/ghostEleft.png')
            self.rect.x -= 1
        if self.rect.x == 80 or self.rect.y == 40 or self.rect.y == self.game.height - 150 or self.rect.x == self.game.width - 160:
            if self.rect.x == 80:
                self.rect.x += 1
            if self.rect.x == self.game.width - 160:
                self.rect.x -= 1
            if self.rect.y == 40:
                self.rect.y += 1
            if self.rect.y == self.game.height - 150:
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
        self.game.screen.blit(self.image, self.rect)

    def respawn(self):
        return self.collides_with(self.bomber_rect)

