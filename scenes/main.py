from objects.bomberman import Bomberman
from objects.field import Field
from scenes.base import Scene
from objects.ghosts import Ghost
from objects.score import Score


class MainScene(Scene):
    def create_objects(self):
        self.ghosts = [Ghost(self.game) for _ in range(5)]
        self.bomberman = Bomberman(self.game)
        self.score = Score(self.game)
        self.field = Field(self.game)
        self.objects = [self.field] + [self.bomberman] + self.ghosts + [self.score]

    def additional_logic(self):
        self.process_ghost_collisions()


    def process_ghost_collisions(self):
        for ghost in self.ghosts:  # Коллизия бомбермэна с призраками
            if ghost.collides_with(self.bomberman):
                print('col')
