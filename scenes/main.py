from constants import Color

from objects.text import Text
from scenes.base import Scene
from objects.ghosts import Ghost

class MainScene(Scene):
    MAX_COLLISIONS = 15

    def create_objects(self):
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.ghosts = [Ghost(self.game) for _ in range(5)]
        self.objects = [self.text_count] + self.ghosts

    def additional_logic(self):
        self.process_ghost_collisions()

        if self.game.wall_collision_count >= self.MAX_COLLISIONS:
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)

    def process_ghost_collisions(self):
        pass