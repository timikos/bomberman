"""
Сцена <Лучший счёт>
Класс FinalScene

Описание: данный класс реализует сцену с лучшим счётом
"""
from constants import Color
from objects.score import HighScoreTable
from scenes.base import Scene
from objects.buttons import ButtonAnimation


class FinalScene(Scene):
    MAX_TICKS = 300
    filename = 'score.txt'

    def __init__(self, game):
        self.seconds_left = self.MAX_TICKS // 100
        super().__init__(game)

    def create_objects(self):
        """Создание объектов"""
        self.highscore = HighScoreTable(self.game, self.filename)
        self.button_exit = ButtonAnimation(self.game, (350, 495, 100, 40), Color.WHITE, 'Выход', self.exit)

        """Список объектов"""
        self.objects = [self.highscore, self.button_exit]

    def exit(self):
        """Выход"""
        self.game.game_over = True
