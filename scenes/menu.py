"""
Сцена <Главное меню>
Класс MenuScene

Описание: данный класс реализует сцену с главным меню
"""

from constants import Color
from objects.buttons import ButtonAnimation
from scenes.base import Scene
from objects.background import Background

class MenuScene(Scene):
    def create_objects(self):
        """Создание объектов"""
        self.button_start = ButtonAnimation(self.game, (350, 425, 100, 40), Color.WHITE, "Запуск игры", self.set_main_scene)
        self.button_info = ButtonAnimation(self.game, (350, 475, 100, 40), Color.WHITE, "Управление", self.set_info_scene)
        self.Background=Background(self.game, (0, 0))
        self.button_exit = ButtonAnimation(self.game, (350, 525, 100, 40), Color.WHITE, 'Выход', self.exit)

        """Список объектов"""
        self.objects = [self.Background, self.button_start, self.button_info, self.button_exit]

    def set_main_scene(self):
        """Переход на сцену игры"""
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_info_scene(self):
        """Переход на сцену с информацией"""
        self.set_next_scene(self.game.INFO_SCENE_INDEX)

    def exit(self):
        """Выход"""
        self.game.game_over = True