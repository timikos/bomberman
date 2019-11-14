from constants import Color

from objects.bomberman import Bomberman
from objects.field import Field
from objects.text import Text
from scenes.base import Scene


class MainScene(Scene):
    MAX_COLLISIONS = 15

    def create_objects(self):
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.bomberman = Bomberman(self.game)
        self.field = Field(self.game)
        self.objects = [self.field] + [self.text_count] + [self.bomberman]

    def additional_logic(self):
        self.text_count.update_text(
            'Коллизии со стенами: {}/{}'.format(
                self.game.wall_collision_count,
                self.MAX_COLLISIONS
            )
        )
        if self.game.wall_collision_count >= self.MAX_COLLISIONS:
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)
