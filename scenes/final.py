from constants import Color
from objects.score import HighScoreTable
from scenes.base import Scene
from objects.button_animated import BtnAnim


class FinalScene(Scene):
    MAX_TICKS = 300

    def __init__(self, game):
        self.seconds_left = self.MAX_TICKS // 100
        super().__init__(game)


    def create_objects(self):
        self.highscore = HighScoreTable(self.game, 'score.txt')
        self.button_exit = BtnAnim(self.game, (350, 495, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.highscore, self.button_exit]


    def exit(self):
        self.game.game_over = True

