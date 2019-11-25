import pygame

from constants import Color
from objects.base import DrawObject

class Timer(DrawObject):
    MAX_TIME_SECONDS = 12000
    TIMER_GAMEOVER = 'Time: {}'
    POS_X = 10
    POS_Y = 10

    def __init__(self, game):
        super().__init__(game)
        self.start_ticks = 0
        self.seconds = self.MAX_TIME_SECONDS // 100
        print(self.seconds)

    def get_timer_text(self):
        return self.TIMER_GAMEOVER.format(self.seconds)


    def timer_update(self):
        font_timer = pygame.font.Font(None, 36)
        text_timer = font_timer.render(self.get_timer_text(), 1, Color.RED)
        self.game.screen.blit(text_timer, (self.POS_X, self.POS_X))

    def process_logic(self):
        self.game.ticks += 1
        seconds = self.MAX_TIME_SECONDS // 100 - self.game.ticks // 100
        if seconds > 0:
            print(self.seconds)
            self.seconds = seconds
            self.timer_update()
        else:
            self.game.game_over = True

