from constants import Color

from objects.bomberman import Bomberman
from objects.field import Field
from objects.text import Text
from scenes.base import Scene
from objects.ghosts import Ghost

class MainScene(Scene):

    def create_objects(self):
        self.ghosts = [Ghost(self.game) for _ in range(5)]
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.bomberman = Bomberman(self.game)
        self.field = Field(self.game)
        self.objects = [self.field] + [self.text_count] + [self.bomberman] + self.ghosts

    def additional_logic(self):
        self.process_ghost_collisions()


    def process_ghost_collisions(self):
        pass
