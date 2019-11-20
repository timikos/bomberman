import pygame
from objects.bomberman import Bomberman
from objects.field import Field
from scenes.base import Scene
from objects.ghosts import Ghost
from objects.blocks import TileMap, DestroyableTileMap
from objects.score import Score, ScorePos
from objects.door import Door
from objects.bombs import Bomb
from constants import Color
from objects.modifier import SpeedModifier


class MainScene(Scene):
    def create_objects(self):

        self.bomberman = Bomberman(self.game)
        self.ghosts = [Ghost(self.game) for _ in range(5)]
        self.score = Score(self.game)
        self.health = Score(self.game, Color.RED, 5, 60, ScorePos.LEFT_BOTTOM, "Health: ", text_after="", border_shift=(10, 10))
        self.field = Field(self.game)
        self.tilemap = TileMap(self.game)
        self.block = DestroyableTileMap(self.game)
        self.door = Door(self.game)
        self.bomb = Bomb(self.game)
        self.modifiers = [SpeedModifier(self.game, 80, 80), SpeedModifier(self.game, 160, 160)]
        self.objects = [self.field] + [self.tilemap] + [self.block] + [self.bomberman] + self.ghosts + [self.score] + \
                       [self.health] + [self.door] + [self.bomb] + self.modifiers
        self.modifier_effects = {}

    def additional_logic(self):
        self.process_ghost_collisions()
        self.process_door_collisions()
        self.process_ghost_collisions_bomb()
        self.process_modifiers_collisions()
        self.process_show_door()
        self.process_game_lose()
        self.process_bomberman_collision_bomb_fire()
        self.process_modifiers_effects()
        self.process_bomb_detection()

    def process_ghost_collisions(self):
        for ghost in self.ghosts:  # Коллизия бомбермэна с призраками
            if ghost.collides_with(self.bomberman):
                self.respawn_bomberman_after_collision()

    def process_bomb_detection(self):
        """
        delta_x = abs(((self.bomberman.rect.x + self.bomberman.rect.width//2) // 40) - (self.block1.x // 40))
        delta_y = abs(((self.bomberman.rect.y - self.bomberman.rect.height//2) // 40) - ((self.block1.y - 40) // 40))
        #print(delta_x, delta_y)
        if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
            self.block1.readyToBreak = True
        else:
            self.block1.readyToBreak = False
        """

        for row in self.block.tiles:
            for tile in row:
                delta_x = abs(((self.bomb.rect.x + self.bomb.rect.width // 2) // 40) - (tile.x // 40))
                delta_y = abs(((self.bomb.rect.y - self.bomb.rect.height // 2) // 40) - ((tile.y - 40) // 40))
                if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
                    tile.readyToBreak = True
                else:
                    tile.readyToBreak = False

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

    def process_game_lose(self):
        if self.health.count == 0:
            self.score.write_to_file()
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)  # Добавлено на время

    def process_door_collisions(self):
        # Бомбермэн входит в дверь
        if self.door.collides_with(self.bomberman):
            self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)
            self.score.write_to_file()


    def process_bomberman_collision_bomb_fire(self):
        if self.bomberman.collides_with(self.bomb.fire_rects[0]):
                self.respawn_bomberman_after_collision()
        elif self.bomberman.collides_with(self.bomb.fire_rects[1]):
                self.respawn_bomberman_after_collision()
        elif self.bomberman.collides_with(self.bomb.fire_rects[2]):
                self.respawn_bomberman_after_collision()
        elif self.bomberman.collides_with(self.bomb.fire_rects[3]):
                self.respawn_bomberman_after_collision()

    def respawn_bomberman_after_collision(self):
        self.health.sub(1)
        self.bomberman.rect.x = 400
        self.bomberman.rect.y = 300

    def process_modifiers_collisions(self):
        for modifier in self.modifiers:
            if modifier.collides_with(self.bomberman):
                modifier.hide()
                self.modifier_effects['speed'] = pygame.time.get_ticks()

    def process_modifiers_effects(self):
        print(self.modifier_effects)

        for effect in self.modifier_effects:
            if self.modifier_effects[effect] + 10000 <= pygame.time.get_ticks():
                self.modifier_effects[effect] = 0

        if self.modifier_effects.get('speed', 0):
            self.bomberman.speed = 10
        else:
            self.bomberman.speed = 5



"""
    Метод коллизии призраков со стенкой

    def process_ghost_collisions_with_wall(self):
        for ghost in self.ghosts:
            if ghost.collides_with(<стенка>):
                ghost.start_move()
"""
