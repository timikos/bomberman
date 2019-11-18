from constants import Color
from objects.button_animated import BtnAnim
from scenes.base import Scene
from objects.background import Background

class MenuScene(Scene):
    def create_objects(self):
        self.button_start = BtnAnim(self.game, (350, 405, 100, 40), Color.WHITE, "Запуск игры", self.set_main_scene)
        self.Background=Background(self.game, 'images/main_menu.png', (0, 0))
        self.button_info = BtnAnim(self.game, (350, 455, 100, 40), Color.WHITE, "Инструкция", self.set_info_scene)
        self.button_exit = BtnAnim(self.game, (350, 505, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.Background, self.button_start, self.button_info, self.button_exit]

    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_info_scene(self):
        self.set_next_scene(self.game.INFO_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True