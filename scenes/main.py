import pygame
from objects.bomberman import Bomberman
from objects.field import Field
from scenes.base import Scene
from objects.ghosts import Ghost, SpeedGhost, SuperGhost
from objects.blocks import TileMap, DestroyableTileMap
from objects.score import Score, ScorePos
from objects.door import Door
from objects.bombs import Bomb
from constants import Color, ScoreProperties
from objects.modifier import SpeedModifier
from Global import Globals


class MainScene(Scene):

    def create_objects(self):

        self.bomberman = Bomberman(self.game)
        self.ghosts = [Ghost(self.game) for _ in range(2)] + [SpeedGhost(self.game) for _ in range(2)] + \
                      [SuperGhost(self.game)]
        self.score = Score(self.game)
        self.health = Score(self.game, Color.RED, 5, 60, ScorePos.LEFT_BOTTOM, "Health: ", text_after="",
                            border_shift=(10, 10))
        self.field = Field(self.game)
        self.fields = [Field(self.game) for _ in range(5)]
        self.tilemap = TileMap(self.game)
        self.dstr_tilemap = DestroyableTileMap(self.game)
        self.door = Door(self.game)
        self.bomb = Bomb(self.game)
        self.modifiers = [SpeedModifier(self.game, 82, 82), SpeedModifier(self.game, 162, 162)]
        self.objects = [self.field] + [self.bomb] + [self.dstr_tilemap] + [self.tilemap] + \
                       [self.bomberman] + self.ghosts + \
                       [self.score] + [self.health] + \
                       [self.door] + self.modifiers

        self.modifier_effects = {}
        self.unneeded_blocks_deletion()

    def additional_logic(self):
        self.process_ghost_collisions_with_bomberman()
        self.process_ghost_collisions_with_bomb()
        self.process_ghost_collisions_with_destroyable_tiles()
        self.process_door_collisions_with_bomberman()
        self.process_show_door()
        self.process_bomberman_collision_with_bomb_fire()
        self.process_bomberman_collision_with_blocks()
        self.process_modifiers_effects()
        self.process_bomb_detection()
        self.process_modifiers_collisions_with_bomberman()
        self.process_game_lose()
        self.process_bomberman_collision_with_d_blocks()

    def process_ghost_collisions_with_bomberman(self):
        for ghost in self.ghosts:  # Коллизия бомбермэна с призраками
            if ghost.collides_with(self.bomberman) and not self.bomberman.is_invulnerable():
                self.respawn_bomberman_after_collision()

    def process_bomb_detection(self):
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                for fire_rect in self.bomb.bomb_fire.fire_rects:
                    if tile.collides_with(fire_rect):
                        tile.start_ticks = pygame.time.get_ticks()
                        tile.readyToBreak = True

    def process_ghost_collisions_with_bomb(self):
        for ghost in self.ghosts:
            for fire_rect in self.bomb.bomb_fire.fire_rects:
                if ghost.collides_with(fire_rect):
                    ghost.hidden = True
                    self.score.add(100)

    def process_ghost_collisions_with_destroyable_tiles(self):
        for row in self.dstr_tilemap.tiles:
            for tile in row:
                for ghost in self.ghosts:
                    if tile.collides_with(ghost.rect) and not ghost.pass_throw_destruct_blocks:
                        ghost.start_move()

    def process_show_door(self):
        if self.score.count == 500:
            self.door.show_door()

    def process_game_lose(self):
        if self.health.count == 0:
            self.game.scenes[self.game.STATISTICS_SCENE_INDEX].set_info([
                ['Заработано очков', self.score.count, self.score.count],
                ['Жизней осталось', self.health.count, self.health.count * ScoreProperties.HEALTH]
            ])
            self.set_next_scene(self.game.STATISTICS_SCENE_INDEX)
            # self.score.write_to_file()
            # self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)

    def process_door_collisions_with_bomberman(self):
        if self.door.collides_with(self.bomberman):
            self.game.scenes[self.game.STATISTICS_SCENE_INDEX].set_info([
                ['Заработано очков', self.score.count, self.score.count],
                ['Жизней осталось', self.health.count, self.health.count * ScoreProperties.HEALTH]
            ])
            self.set_next_scene(self.game.STATISTICS_SCENE_INDEX)
            # self.score.write_to_file()
            # self.set_next_scene(self.game.GAMEOVER_SCENE_INDEX)

    def process_bomberman_collision_with_bomb_fire(self):
        for fire_rect in self.bomb.bomb_fire.fire_rects:
            if self.bomberman.collides_with(fire_rect) and not self.bomberman.is_invulnerable():
                self.respawn_bomberman_after_collision()

    def respawn_bomberman_after_collision(self):
        self.health.sub(1)
        self.bomberman.rect.x = 400
        self.bomberman.rect.y = 300
        self.bomberman.start_ticks = pygame.time.get_ticks()  # Запускает счеткик (персонаж неузвим 3 секунды)

    def process_modifiers_collisions_with_bomberman(self):
        for modifier in self.modifiers:
            if modifier.collides_with(self.bomberman):
                modifier.hide()
                self.modifier_effects['speed'] = pygame.time.get_ticks()

    def process_modifiers_effects(self):
        for effect in self.modifier_effects:
            if self.modifier_effects[effect] + 10000 <= pygame.time.get_ticks():
                self.modifier_effects[effect] = 0

        if self.modifier_effects.get('speed', 0):
            self.bomberman.speed = 10
        else:
            self.bomberman.speed = 5

    def process_bomberman_collision_with_blocks(self):
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
