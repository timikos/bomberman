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
from constants import Color, ScoreProperties
from objects.modifier import SpeedModifier, BombPowerModifier, AddLifeModifier
from Global import Globals


class MainScene(Scene):
    def create_objects(self):
        """Создание объектов"""
        self.bomberman = Bomberman(self.game)
        self.ghosts = [Ghost(self.game) for _ in range(2)] + [SpeedGhost(self.game) for _ in range(2)] + \
                      [SuperGhost(self.game)]
        self.score = Score(self.game)
        self.health = Score(self.game, Color.RED, 5, 60, ScorePosition.LEFT_BOTTOM, "Health: ", text_after="",
                            border_shift=(10, 10))
        self.field = Field(self.game)
        self.fields = [Field(self.game) for _ in range(5)]
        self.tilemap = IndestructibleBlockMap(self.game)
        self.dstr_tilemap = DestroyedBlockMap(self.game)
        self.door = Door(self.game)
        self.bomb_list = BombsList(self.game)
        self.timer = Timer(self.game)
        self.text_count = Text(self.game, text='', color=Color.RED, x=400, y=550)
        self.modifiers = [SpeedModifier(self.game, 82, 82),
                          SpeedModifier(self.game, 162, 162),
                          BombPowerModifier(self.game, 350, 350),
                          BombPowerModifier(self.game, 450, 450),
                          AddLifeModifier(self.game, 250, 250),
                          AddLifeModifier(self.game, 500, 300)]
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
        """Разрушение блоков от бомбы"""
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                for bomb in self.bomb_list.bombs:
                    for fire_rect in bomb.bomb_fire.fire_rects:
                        if tile.collides_with(fire_rect):
                            tile.start_ticks = pygame.time.get_ticks()
                            tile.readyToBreak = True

    def process_ghost_collisions_with_fire_bomb(self):
        """Коллизия врагов с огнём бомбы"""
        for ghost in self.ghosts:
            for bomb in self.bomb_list.bombs:
                for fire_rect in bomb.bomb_fire.fire_rects:
                    if ghost.collides_with(fire_rect):
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
            for fire_rect in bomb.bomb_fire.fire_rects:
                if self.bomberman.collides_with(fire_rect) and not self.bomberman.is_invulnerable():
                    self.respawn_bomberman_after_collision()

    def process_bomberman_collision_with_modifiers(self):
        """Коллизия главного героя с модификаторами"""
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
                            Globals.FieldPosition -= self.bomberman.speed
                            self.process_all_draw()
                            print(Globals.FieldPosition)
                    elif self.bomberman.current_shift_x < 0:
                        while tile.collides_with(self.bomberman.rect):
                            Globals.FieldPosition += self.bomberman.speed
                            self.process_all_draw()
                    elif self.bomberman.current_shift_y > 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.y -= 1
                    elif self.bomberman.current_shift_y < 0:
                        while tile.collides_with(self.bomberman.rect):
                            self.bomberman.rect.y += 1
                    self.bomberman.current_shift_x = 0
                    self.bomberman.current_shift_y = 0

    def process_bomberman_collision_with_d_blocks(self):
        """Коллизия главного героя с разрушаемыми блоками"""
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                if tile.collides_with(self.bomberman.rect):
                    if self.bomberman.current_shift_x > 0:
                        while tile.collides_with(self.bomberman.rect):
                            Globals.FieldPosition -= self.bomberman.speed
                            self.process_all_draw()
                    elif self.bomberman.current_shift_x < 0:
                        while tile.collides_with(self.bomberman.rect):
                            Globals.FieldPosition += self.bomberman.speed
                            self.process_all_draw()
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