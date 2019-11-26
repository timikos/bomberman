import pygame

from constants import Color, InterfaceProperties
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
        self.text_timer = None

    def get_timer_text(self):
        return self.TIMER_GAMEOVER.format(self.seconds)


    def timer_update(self):
        font_timer = pygame.font.Font(InterfaceProperties.TEXT_FONT, InterfaceProperties.FONT_SIZE)
        self.text_timer = font_timer.render(self.get_timer_text(), 1, Color.RED)

    def get_width(self):
        return self.text_timer.get_width()

    def get_height(self):
        return self.text_timer.get_height()

    def process_logic(self):
        self.game.ticks += 1
        seconds = self.MAX_TIME_SECONDS // 100 - self.game.ticks // 100
        if seconds > 0:
            self.seconds = seconds
            self.timer_update()
        else:
            self.game.game_over = True

    def process_draw(self):
        self.game.screen.blit(self.text_timer, (self.game.width // 2 - self.get_width() // 2, self.game.height - self.get_height() - 10))

