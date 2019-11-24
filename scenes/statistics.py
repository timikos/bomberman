from constants import Color
from objects.button_animated import BtnAnim
from scenes.base import Scene
from objects.score import StatisticsTable


class StatisticsScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def set_info(self, info):
        self.table.set_info(info, True)

    def create_objects(self):
        self.button_continue = BtnAnim(self.game, (350, 495, 100, 40), Color.WHITE, 'Продолжить', self.next)
        self.table = StatisticsTable(self.game)
        self.objects = [self.button_continue, self.table]

    def next(self):
        self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)
