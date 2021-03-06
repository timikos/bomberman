"""
Класс Timer

Описание: данный класс реализует таймер с обратным отсчётом
"""
import pygame
from constants import Color, InterfaceProperties, TimerProperties
from objects.base import DrawObject


class Timer(DrawObject):
    """Таймер"""

    def __init__(self, game, max_time_seconds=TimerProperties.MAX_TIME_SECONDS, text='Time: {}'):
        super().__init__(game)
        self.max_time_seconds = max_time_seconds
        self.text = text
        self.start_ticks = 0
        self.seconds = self.max_time_seconds // 100
        self.text_timer = None
        self.font_timer = pygame.font.Font(InterfaceProperties.TEXT_FONT, InterfaceProperties.FONT_SIZE - 20)
        self.text2 = "Время выходит!"
        self.timer_update()

    def get_timer_text(self):
        """Добавление в текст счётчика"""
        return self.text.format(self.seconds)

    def timer_update(self):
        """Обновление таймера"""
        self.text_timer = self.font_timer.render(self.get_timer_text(), 1, Color.RED)
        self.text_end = self.font_timer.render(self.text2, 1, Color.RED)

    def get_width(self):
        """Получение ширины"""
        return self.text_timer.get_width()

    def get_height(self):
        """Получение высоты"""
        return self.text_timer.get_height()

    def process_logic(self):
        """Обработка логики"""
        self.game.ticks += 1
        seconds = self.max_time_seconds // 100 - self.game.ticks // 100
        if seconds > 0:
            self.seconds = seconds
            self.timer_update()
        else:  # Окончание таймера
            self.game.current_scene = 2

    def get_position(self):
        return [self.game.width // 2 - self.get_width() // 2, self.game.height - self.get_height() - 10]

    def process_draw(self):
        self.game.screen.blit(self.text_timer, self.get_position())
        if self.seconds < 30:
            self.game.screen.blit(self.text_end, (self.game.scenes[1].bomberman.x // 2 + 75,
                                                0))
