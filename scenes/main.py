"""
Сцена <Игра>
Класс MainScene

Описание: данный класс реализует геймплей
"""

import pygame
from objects.bomberman import Bomberman
from objects.field import Field
from objects.text import Text
from objects.timer import Timer
from scenes.base import Scene
from objects.ghosts import Ghost, SpeedGhost, SuperGhost
from objects.blocks import IndestructibleBlockMap, DestroyedBlockMap
from objects.score import Score, ScorePosition
from objects.door import Door
from objects.bombs import BombsList
from objects.modifier import SpeedModifier, BombPowerModifier, AddLifeModifier, MultiBombModifier
from constants import Color, ScoreProperties, FieldProperties

from Global import Globals
import json


class MainScene(Scene):

    def __init__(self, game, level_num=0):
        file_name = 'levels/level' + str(level_num) + '.json'
        with open(file_name, 'r') as f:
            data = json.load(f)
            self.level_data = data
        super().__init__(game)


    def create_objects(self):
        """Создание объектов"""
        self.bomberman = Bomberman(self.game)
        self.score = Score(self.game)
        self.health = Score(self.game, Color.RED, 5, 60, ScorePosition.LEFT_BOTTOM, "Health: ", text_after="",
                            border_shift=(10, 10))
        self.field = Field(self.game, ground_texture=self.level_data['ground_texture'])
        self.ghosts = []
        self.modifiers = []

        self.modifiers = [SpeedModifier(self.game, 82, 82),
                          SpeedModifier(self.game, 162, 162),
                          BombPowerModifier(self.game, 350, 350),
                          BombPowerModifier(self.game, 450, 450),
                          AddLifeModifier(self.game, 250, 250),
                          AddLifeModifier(self.game, 500, 300),
                          MultiBombModifier(self.game, 200, 200),
                          MultiBombModifier(self.game, 400, 400),
                          AddLifeModifier(self.game, 500, 300)]

        for obj in self.level_data['objects']:
            x, y = self.field.x + int(obj['pos']['x']) * FieldProperties.CELL_LENGTH, \
                   self.field.y + int(obj['pos']['y']) * FieldProperties.CELL_LENGTH
            if obj['type'] == 'ghost':
                t = obj['data']['type']
                c = None
                if t == 'usual':
                    c = Ghost
                elif t == 'speed':
                    c = SpeedGhost
                elif t == 'super':
                    c = SuperGhost
                self.ghosts += [c(game=self.game, x=x, y=y)]
            elif obj['type'] == 'modifier':
                t = obj['data']['type']
                c = None
                if t == 'speed':
                    c = SpeedModifier
                elif t == 'bomb_power':
                    c = BombPowerModifier
                elif t == 'add_life':
                    c = AddLifeModifier
                self.modifiers += [c(game=self.game, x=x, y=y)]

        self.tilemap = IndestructibleBlockMap(self.game)
        self.dstr_tilemap = DestroyedBlockMap(self.game)
        self.door = Door(self.game)
        self.bomb_list = BombsList(self.game)
        self.timer = Timer(self.game)
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)

        self.modifier_effects = {}
        self.unneeded_blocks_deletion()
        """Список объектов"""
        self.objects = [self.field] + [self.bomb_list] + [self.dstr_tilemap] + [self.tilemap] + \
                       [self.bomberman] + self.ghosts + \
                       [self.score] + [self.health] + \
                       [self.door] + self.modifiers + [self.timer]



    def additional_logic(self):
        """Все процессы"""
        self.process_ghost_collisions_with_bomberman()
        self.process_ghost_collisions_with_fire_bomb()
        self.process_ghost_collisions_with_destroyable_tiles()
        self.process_bomberman_collision_with_door()
        self.process_bomberman_collision_with_bomb_fire()
        self.process_bomberman_collision_with_blocks()
        self.process_bomberman_collision_with_modifiers()
        self.process_bomberman_collision_with_d_blocks()
        self.process_modifiers_effects()
        self.process_bomb_detection()
        self.process_show_door()
        self.process_game_lose()

    def process_ghost_collisions_with_bomberman(self):
        """Коллизия бомбермэна с призраками"""
        for ghost in self.ghosts:
            if ghost.collides_with(self.bomberman) and not self.bomberman.is_invulnerable():
                self.respawn_bomberman_after_collision()

    def process_bomb_detection(self):
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                for bomb in self.bomb_list.bombs:
                    for fire in bomb.bomb_fire.fire_rects:
                        if tile.collides_with(fire.fire_rect) and fire.active:
                            tile.start_ticks = pygame.time.get_ticks()
                            tile.readyToBreak = True

    def process_ghost_collisions_with_fire_bomb(self):
        """Коллизия врагов с огнём бомбы"""
        for ghost in self.ghosts:
            for bomb in self.bomb_list.bombs:
                for fire in bomb.bomb_fire.fire_rects:
                    if ghost.collides_with(fire.fire_rect) and fire.active:
                        ghost.hidden = True
                        self.score.add_count(100)

    def process_ghost_collisions_with_destroyable_tiles(self):
        """Коллизия врагов с разрушаемыми блоками"""
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                for ghost in self.ghosts:
                    if tile.collides_with(ghost.rect) and not ghost.pass_throw_destruct_blocks:
                        ghost.start_move()

    def process_ghost_collision_with_wall(self):
        """Коллизия призраков с блоком"""
        for ghost in self.ghosts:
            if ghost.collides_with(self.tilemap.tiles):
                ghost.start_move()


    def process_bomberman_collision_with_door(self):
        """Коллизия бомбермена с дверью"""
        if self.bomberman.collides_with(self.door):
            self.game.scenes[self.game.STATISTICS_SCENE_INDEX].set_info([
                ['Заработано очков', self.score.count, self.score.count],
                ['Жизней осталось', self.health.count, self.health.count * ScoreProperties.HEALTH]
            ])
            self.set_next_scene(self.game.STATISTICS_SCENE_INDEX)


    def process_bomberman_collision_with_bomb_fire(self):
        """Коллизия главного героя с огнём от бомбы"""
        for bomb in self.bomb_list.bombs:
            for fire in bomb.bomb_fire.fire_rects:
                if self.bomberman.collides_with(fire.fire_rect) and fire.active and not self.bomberman.is_invulnerable():
                    self.respawn_bomberman_after_collision()

    def respawn_bomberman_after_collision(self):
        self.health.sub(1)
        Globals.FieldPosition = 400
        self.bomberman.rect.x = 400
        self.bomberman.rect.y = 300

    def process_bomberman_collision_with_modifiers(self):
        """Коллизия главного героя с модификаторами"""
        for modifier in self.modifiers:
            if modifier.collides_with(self.bomberman):
                modifier.hide()
                self.modifier_effects[modifier.name] = pygame.time.get_ticks()

    def process_modifiers_collisions_with_bomberman(self):
        for modifier in self.modifiers:
            if modifier.collides_with(self.bomberman):
                modifier.hide()
                self.modifier_effects[modifier.name] = pygame.time.get_ticks()

    def process_bomberman_collision_with_blocks(self):
        """Коллизия главного героя с неразрушаемыми блоками"""
        for row in self.tilemap.tiles:
            for tile in row:
                if tile.collides_with(self.bomberman.rect):
                    if self.bomberman.current_shift_x > 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.x -= 1
                    elif self.bomberman.current_shift_x < 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.x += 1
                    elif self.bomberman.current_shift_y > 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.y -= 1
                    elif self.bomberman.current_shift_y < 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.y += 1
                    self.bomberman.current_shift_x = 0
                    self.bomberman.current_shift_y = 0

    def process_bomberman_collision_with_d_blocks(self):
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                if tile.collides_with(self.bomberman.rect):
                    if self.bomberman.current_shift_x > 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.x -= 1
                    elif self.bomberman.current_shift_x < 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.x += 1
                    elif self.bomberman.current_shift_y > 0:
                        if self.bomberman.speed == 5:
                            self.bomberman.rect.y -= 5
                        elif self.bomberman.speed == 10:
                            self.bomberman.rect.y -= 10
                    elif self.bomberman.current_shift_y < 0:
                        if self.bomberman.speed == 5:
                            self.bomberman.rect.y += 5
                        elif self.bomberman.speed == 10:
                            self.bomberman.rect.y += 10
                    self.bomberman.current_shift_x = 0
                    self.bomberman.current_shift_y = 0


    def respawn_bomberman_after_collision(self):
        """Респавн главного героя"""
        self.health.sub_count(1)
        self.bomberman.rect.x = self.bomberman.rect.x
        self.bomberman.rect.y = self.bomberman.rect.y
        self.bomberman.start_ticks = pygame.time.get_ticks()  # Запускает счеткик (персонаж неузвим 3 секунды)


    def process_modifiers_effects(self):
        """Эффекты модификаторов"""
        for effect in self.modifier_effects:
            if self.modifier_effects[effect] + 10000 <= pygame.time.get_ticks():
                self.modifier_effects[effect] = 0

        if self.modifier_effects.get('speed', 0):
            self.bomberman.speed = 10
        else:
            self.bomberman.speed = 5
        if self.modifier_effects.get('bomb_power', 0):
            self.bomberman.bomb_power = 2
        else:
            self.bomberman.bomb_power = 1
        if self.modifier_effects.get('add_life', 0):
            self.health.add_count(1)
            self.modifier_effects['add_life'] = 0
        if self.modifier_effects.get('multi_bomb', 0):
            self.bomberman.multi_bomb = True
        else:
            self.bomberman.multi_bomb = False


    def process_show_door(self):
        """Условие открытие двери"""
        if self.score.count == 500:
            self.door.show_door()

    def process_game_lose(self):
        """Условие проигрыша"""
        if self.health.count == 0:
            self.game.scenes[self.game.STATISTICS_SCENE_INDEX].set_info([
                ['Заработано очков', self.score.count, self.score.count],
                ['Жизней осталось', self.health.count, self.health.count * ScoreProperties.HEALTH]
            ])
            self.set_next_scene(self.game.STATISTICS_SCENE_INDEX)

    def unneeded_blocks_deletion(self):
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                delta_x = abs(((self.bomberman.rect.x + self.bomberman.rect.width // 2) // 40) - (tile.x // 40))
                delta_y = abs(((self.bomberman.rect.y - self.bomberman.rect.height // 2) // 40) - ((tile.y - 40) // 40))
                if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
                    tile.isDestroyed = True
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                for ghost in self.ghosts:
                    delta_x = abs(((ghost.rect.x + ghost.rect.width // 2) // 40) - (tile.x // 40))
                    delta_y = abs(((ghost.rect.y - ghost.rect.height // 2) // 40) - ((tile.y - 40) // 40))
                    if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
                        tile.isDestroyed = True

    def process_ghost_collisions_with_wall(self):
        for ghost in self.ghosts:
            if ghost.collides_with(self.tilemap.tiles):
                ghost.start_move()
'''
    Метод коллизии призраков со стенкой
'''

