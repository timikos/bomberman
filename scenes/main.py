import pygame

from objects.bomberman import Bomberman
from objects.field import Field
from scenes.base import Scene
from objects.ghosts import Ghost
from objects.blocks import TileMap
from objects.score import Score
from objects.door import Door
from objects.bombs import Bomb


class MainScene(Scene):

    def create_objects(self):
        self.bomberman = Bomberman(self.game)
        self.ghosts = [Ghost(self.game) for _ in range(5)]
        self.score = Score(self.game)
        self.field = Field(self.game)
        self.tilemap = TileMap(self.game)
        self.door = Door(self.game)
        self.bomb = Bomb(self.game)
        self.objects = [self.field] + [self.tilemap] + [self.bomberman] + self.ghosts + [self.score] + [self.door] + [self.bomb]


    def additional_logic(self):
        self.process_ghost_collisions()
        self.process_door_collisions()
        self.process_ghost_collisions_bomb()
        self.process_show_door()

    def process_ghost_collisions(self):
        for ghost in self.ghosts:  # Коллизия бомбермэна с призраками
            if ghost.collides_with(self.bomberman):
                print('col')
                self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)  # Добавлено на время

    def process_ghost_collisions_bomb(self):
        for ghost in self.ghosts:  # Коллизия бомбы с призраками
            if ghost.collides_with(self.bomb.fire_rects[0]):
                ghost.hidden = True
                self.score.add(1)
            elif ghost.collides_with(self.bomb.fire_rects[1]):
                ghost.hidden = True
                self.score.add(1)
            elif ghost.collides_with(self.bomb.fire_rects[2]):
                ghost.hidden = True
                self.score.add(1)
            elif ghost.collides_with(self.bomb.fire_rects[3]):
                ghost.hidden = True
                self.score.add(1)

    def process_show_door(self):
        if self.score.count == 5:
            self.door.show_door()

    def process_door_collisions(self):
        # Бомбермэн входит в дверь
        if self.door.collides_with(self.bomberman):
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)




"""
    Метод коллизии призраков со стенкой

    def process_ghost_collisions_with_wall(self):
        for ghost in self.ghosts:
            if ghost.collides_with(<стенка>):
                ghost.start_move()
"""