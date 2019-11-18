from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.text import Text

class InfoScene(Scene):
    def create_objects(self):
        self.Text = Text(self.game, 280, 255, 'Инструкция: Инструкция', 25, (255, 255, 255))
        self.button_back = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Назад', self.back)
        self.objects = [self.button_back, self.Text]

    def back(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)