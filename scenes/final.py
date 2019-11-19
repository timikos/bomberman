from constants import Color
from objects.text import Text
from objects.score import HighScoreTable
from scenes.base import Scene
from objects.button_animated import BtnAnim


class FinalScene(Scene):
    MAX_TICKS = 300
    GAMEOVER_FMT = 'Game over ({})'

    def __init__(self, game):
        self.seconds_left = self.MAX_TICKS // 100
        super().__init__(game)

    def get_gameover_str(self):
        return self.GAMEOVER_FMT.format(self.seconds_left)

    def create_objects(self):
        self.text_gameover = Text(self.game, text=self.get_gameover_str(), color=Color.RED, x=310, y=290)
        self.highscore = HighScoreTable(self.game)
        self.button_exit = BtnAnim(self.game, (350, 495, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.text_gameover, self.highscore, self.button_exit]

    def additional_logic(self):
        pass

    def exit(self):
        self.game.game_over = True

