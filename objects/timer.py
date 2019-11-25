import pygame

from constants import Color
from objects.text import Text
from scenes.base import Scene

class Timer(Scene):
    MAX_TIME_SECONDS = 120
    TIMER_GAMEOVER = 'Time: {}'
    POS_X = 10
    POS_Y = 10

    def __init__(self, game):
        self.seconds = self.MAX_TIME_SECONDS // 100
        super().__init__(game)

    def get_timer_text(self):
        return self.TIMER_GAMEOVER.format(self.seconds)

    # def create_objects(self):
    #     self.text_timer = Text(self.game, text=self.get_timer_text(), color=Color.WHITE, x=self.POS_X, y=self.POS_Y)
    #     self.objects = [self.text_timer]

    def timer_update(self):
        font_timer = pygame.font.Font(None, 36)
        text_timer = font_timer.render(self.get_timer_text(), 1, Color.RED)
        self.game.screen.blit(text_timer, (self.POS_X, self.POS_X))

    def time_over(self):
        seconds = self.MAX_TIME_SECONDS// 100 - self.game.ticks // 100
        if seconds < self.seconds_left:
            self.seconds = seconds
            self.text_timer.update_text(self.get_timer_text())
        if self.seconds == 0:
            self.game.game_over = True

