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
from objects.blocks import IndestructibleBlockMap, DestroyedBlock
from objects.score import Score, ScorePosition
from objects.door import Door
from objects.bombs import BombsList
from objects.modifier import SpeedModifier, BombPowerModifier, AddLifeModifier, MultiBombModifier
from constants import Color, ScoreProperties, FieldProperties

from Global import Globals
import json

from scenes.lvls import LvlsScene

class MainScene(Scene):
    print("NOW")
    current_lvl = LvlsScene.cur
    def __init__(self, game):

        print("NOW1")
        file_name = 'levels/level' + str(self.current_lvl) + '.json'
        with open(file_name, 'r') as f:
            data = json.load(f)
            self.level_data = data
        super().__init__(game)


    def create_objects(self):
        print("NOW2")
        """Создание объектов"""
        self.bomberman = Bomberman(self.game)  # Главный герой
        self.score = Score(self.game)  # Счётчик очков
        self.health = Score(self.game, Color.RED, 5, 60, ScorePosition.LEFT_BOTTOM, "Health: ", text_after="",
                            border_shift=(10, 10))   # Счётчик жизней
        self.field = Field(self.game, ground_texture=self.level_data['ground_texture'])  # Поле
        self.ghosts = []  # Список врагов
        self.modifiers = []  # Список модификаторов
        self.blocks = []  # Список блоков
        self.tilemap = IndestructibleBlockMap(self.game)  # Сетка неразрушаемых блоков
        self.door = Door(self.game)  # Дверь
        self.bomb_list = BombsList(self.game)
        self.timer = Timer(self.game)  # Таймер обратного отсчёта
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.modifier_effects = {}  # Словарь эффектов модификаторов
        self.unneeded_blocks_deletion()

        self.load_obj_for_lvl()  # Загрузка всех параметров для объектов уровня
        """Список объектов"""
        self.objects = [self.field] + [self.bomb_list] + self.blocks + [self.tilemap] + \
                       [self.bomberman] + self.ghosts + \
                       [self.score] + [self.health] + \
                       [self.door] + self.modifiers + [self.timer]
        self.no_static_objects = [self.bomberman] + self.ghosts

    def process_all_draw(self, type_of_objects='nonestatic'):
        if Globals.CameraStatus is False:
            super().process_all_draw()
        else:
            for item in self.objects:
                item.process_draw()
            self.additional_draw()
            if type_of_objects == 'nonestatic' and Globals.UpdateDisplay is False and Globals.UpdateNext is False:
                for item in self.no_static_objects:  # Обновление призраков/персонажа
                    rect = pygame.Rect(item.rect.x - item.speed, item.rect.y - item.speed,
                                       item.rect.width + item.speed * 2 + 15, item.rect.height + item.speed * 3)
                    pygame.display.update(rect)
                for item in self.bomb_list.bombs:  # Обновление картинки бомбы (Огней)
                    rect = pygame.Rect(item.rect.x - item.rect.width, item.rect.y - item.rect.height,
                                       item.rect.width * 3, item.rect.height * 3)
                    pygame.display.update(rect)
                for item in self.modifiers:  # Обновление картинки бомбы (Огней)
                    rect = pygame.Rect(item.rect)
                    pygame.display.update(rect)
                # Обновление статистики снизу
                pygame.display.update(pygame.Rect(self.game.width // 2 - self.timer.get_width() // 2,
                                                  self.game.height - self.timer.get_height() - 10,
                                                  self.game.width, self.timer.get_height()))
                #  dstrblocks = self.blocks.get_ready_to_break_blocks()  # Получение блоков с анимацией разрушения
                # for item in dstrblocks:  # Обновление анимации блоков при разрушении
                #     pygame.display.update(item)
            elif Globals.UpdateDisplay is True or Globals.UpdateNext is True:  # Обновление всего экрана
                pygame.display.flip()  # Переворот экрана
                Globals.UpdateNext = False
            self.screen.fill(Color.BLACK)
            pygame.time.wait(10)

    def additional_logic(self):
        """Все процессы"""
        self.process_ghost_collisions_with_bomberman()
        self.process_ghost_collisions_with_fire_bomb()
        self.process_ghost_collisions_with_destroyable_tiles()
        self.process_ghost_collision_with_indestructible_tiles()
        self.process_bomberman_collision_with_door()
        self.process_bomberman_collision_with_bomb_fire()
        self.process_bomberman_collision_with_d_blocks()
        self.process_bomberman_collision_with_modifiers()
        self.process_bomberman_collision_with_blocks()
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
        for tile in self.blocks:
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
                        self.ghosts.remove(ghost)
                        if self.ghosts.__len__() != 0:
                            self.score.add_count(100)

    def process_ghost_collisions_with_destroyable_tiles(self):
        """Коллизия врагов с разрушаемыми блоками"""

        for tile in self.blocks:
            for ghost in self.ghosts:
                if tile.collides_with(ghost.rect) and not ghost.pass_throw_destruct_blocks:
                    print('Монстр столкнулся с разрушаемым блоком')
                    # Если монстр сталкивается с блоком при движении по горизонтали
                    if ghost.current_shift_x:
                        ghost.current_shift_x *= -1
                    # Если монстр сталкивается с блоком при движении по вертикали
                    else:
                        ghost.current_shift_y *= -1

    def process_ghost_collision_with_indestructible_tiles(self):
        """Коллизия призраков с неразрушаемыми блоками"""
        for tile in self.blocks:
            for ghost in self.ghosts:
                if tile.collides_with(ghost.rect) and not ghost.pass_throw_destruct_blocks:
                    print('Монстр столкнулся с неразрушаемым блоком')
                    # Если монстр сталкивается с блоком при движении по горизонтали
                    if ghost.current_shift_x:
                        ghost.current_shift_x *= -1
                    # Если монстр сталкивается с блоком при движении по вертикали
                    else:
                        ghost.current_shift_y *= -1


    def process_ghost_collision_with_wall(self):
        """Коллизия призраков с блоком"""
        for ghost in self.ghosts:
            if ghost.collides_with(self.tilemap.tiles):
                ghost.start_move()


    def process_bomberman_collision_with_door(self):
        """Коллизия бомбермена с дверью"""
        if self.bomberman.collides_with(self.door):
            if self.door.hidden is False:
                self.game.scenes[self.game.STATISTICS_SCENE_INDEX].set_info([
                    ['Заработано очков', self.score.count, self.score.count],
                    ['Жизней осталось', self.health.count, self.health.count * ScoreProperties.HEALTH]
                ])
                self.set_next_scene(self.game.STATISTICS_SCENE_INDEX)

    def process_bomberman_collision_with_bomb_fire(self):
        """Коллизия главного героя с огнём от бомбы"""
        for bomb in self.bomb_list.bombs:
            for fire in bomb.bomb_fire.fire_rects:
                if self.bomberman.collides_with(
                        fire.fire_rect) and fire.active and not self.bomberman.is_invulnerable():
                    self.respawn_bomberman_after_collision()


    def respawn_bomberman_after_collision(self):
        """Респавн главного героя"""
        self.health.sub_count(1)
        self.bomberman.rect.x = self.bomberman.rect.x
        self.bomberman.rect.y = self.bomberman.rect.y
        self.bomberman.start_ticks = pygame.time.get_ticks()  # Запускает счеткик (персонаж неузвим 3 секунды)

    def process_bomberman_collision_with_modifiers(self):
        """Коллизия главного героя с модификаторами"""
        for modifier in self.modifiers:
            if modifier.collides_with(self.bomberman):
                modifier.hide()
                self.modifier_effects[modifier.name] = pygame.time.get_ticks()
                self.modifiers.remove(modifier)
                print(self.bomberman.speed)

    def process_bomberman_collision_with_blocks(self):
        """Коллизия главного героя с неразрушаемыми блоками"""
        for row in self.tilemap.tiles:
            for tile in row:

                if tile.rect.collidepoint(self.bomberman.rect.topleft) and not tile.rect.collidepoint(
                        self.bomberman.rect.topright) and self.bomberman.current_shift_y < 0:
                    self.bomberman.rect.x += 5
                elif tile.rect.collidepoint(self.bomberman.rect.topright) and not tile.rect.collidepoint(
                        self.bomberman.rect.topleft) and self.bomberman.current_shift_y < 0:
                    self.bomberman.rect.x -= 5
                elif tile.rect.collidepoint(self.bomberman.rect.bottomright) and not tile.rect.collidepoint(
                        self.bomberman.rect.bottomleft) and self.bomberman.current_shift_y > 0:
                    self.bomberman.rect.x -= 5
                elif tile.rect.collidepoint(self.bomberman.rect.bottomleft) and not tile.rect.collidepoint(
                        self.bomberman.rect.bottomright) and self.bomberman.current_shift_y > 0:
                    self.bomberman.rect.x += 5

                elif tile.rect.collidepoint(self.bomberman.rect.topright) and not tile.rect.collidepoint(
                        self.bomberman.rect.bottomright) and self.bomberman.current_shift_x > 0:
                    self.bomberman.rect.y += 5
                elif tile.rect.collidepoint(self.bomberman.rect.topleft) and not tile.rect.collidepoint(
                        self.bomberman.rect.bottomleft) and self.bomberman.current_shift_x < 0:
                    self.bomberman.rect.y += 5
                elif tile.rect.collidepoint(self.bomberman.rect.bottomright) and not tile.rect.collidepoint(
                        self.bomberman.rect.topright) and self.bomberman.current_shift_x > 0:
                    self.bomberman.rect.y -= 5
                elif tile.rect.collidepoint(self.bomberman.rect.bottomleft) and not tile.rect.collidepoint(
                        self.bomberman.rect.topleft) and self.bomberman.current_shift_x < 0:
                    self.bomberman.rect.y -= 5
                else:
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
        for tile in self.blocks:
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
        """Условие открытия двери"""
        door_collide = False
        if self.ghosts.__len__() == 0:
            for block in self.blocks:
                if self.door.collides_with(block) and block.isDestroyed is False:
                    door_collide = True
                    print(door_collide)
            if door_collide is False:
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
        for tile in self.blocks:
            delta_x = abs(((self.bomberman.rect.x + self.bomberman.rect.width // 2) // 40) - (tile.x // 40))
            delta_y = abs(((self.bomberman.rect.y - self.bomberman.rect.height // 2) // 40) - ((tile.y - 40) // 40))
            if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
                tile.isDestroyed = True
        for tile in self.blocks:
            for ghost in self.ghosts:
                delta_x = abs(((ghost.rect.x + ghost.rect.width // 2) // 40) - (tile.x // 40))
                delta_y = abs(((ghost.rect.y - ghost.rect.height // 2) // 40) - ((tile.y - 40) // 40))
                if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
                    tile.isDestroyed = True

    def load_obj_for_lvl(self):
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
                elif t == 'multi_bomb':
                    c = MultiBombModifier
                self.modifiers += [c(game=self.game, x=x, y=y)]
            elif obj['type'] == 'block':
                c = DestroyedBlock
                self.blocks += [c(game=self.game, x=x, y=y)]
