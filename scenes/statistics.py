"""
Сцена <Статистика>
Класс StatisticsScene

Описание: данный класс реализует сцену со статистикой после окончания игры
"""
from constants import Color
from objects.buttons import ButtonAnimation
from scenes.base import Scene
from objects.score import StatisticsTable


class StatisticsScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def create_objects(self):
        """Создание объектов"""
        self.button_continue = ButtonAnimation(self.game, (350, 495, 100, 40), Color.WHITE, 'Продолжить', self.next)
        self.table = StatisticsTable(self.game)

        """Список объектов"""
        self.objects = [self.button_continue, self.table]

    def set_info(self, info):
        """Переход на сценку с информацией"""
        self.table.set_info(info, True)

    def next(self):
        """Переходи на следующую сцену"""
        self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)
