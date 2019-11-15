from constants import Color
from objects.text import Text
from scenes.base import Scene


class MainScene(Scene):
    MAX_COLLISIONS = 15

    def create_objects(self):
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.objects = [self.text_count]

    def additional_logic(self):
        self.process_ball_collisions()
        self.text_count.update_text(
            'Коллизии со стенами: {}/{}'.format(
                self.game.wall_collision_count,
                self.MAX_COLLISIONS
            )
        )
        if self.game.wall_collision_count >= self.MAX_COLLISIONS:
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)