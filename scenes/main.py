from objects.bomberman import Bomberman
from objects.field import Field
from scenes.base import Scene
from objects.ghosts import Ghost
from objects.blocks import TileMap, DestroyableTileMap
from objects.score import Score
from objects.bombs import Bomb



class MainScene(Scene):
    def create_objects(self):
        self.ghosts = [Ghost(self.game) for _ in range(5)]
        self.bomberman = Bomberman(self.game)
        self.score = Score(self.game)
        self.field = Field(self.game)
        self.tilemap = TileMap(self.game)
        self.block = DestroyableTileMap(self.game)
        self.objects = [self.field] + [self.tilemap] + [self.block] + [self.bomberman] + self.ghosts + \
                       [self.score]

    def additional_logic(self):
        self.process_ghost_collisions()
        self.process_bomb_detection()

    def process_ghost_collisions(self):
        for ghost in self.ghosts:  # Коллизия бомбермэна с призраками
            if ghost.collides_with(self.bomberman):
                print('col')

    def process_bomb_detection(self):
        '''
        delta_x = abs(((self.bomberman.rect.x + self.bomberman.rect.width//2) // 40) - (self.block1.x // 40))
        delta_y = abs(((self.bomberman.rect.y - self.bomberman.rect.height//2) // 40) - ((self.block1.y - 40) // 40))
        #print(delta_x, delta_y)
        if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
            self.block1.readyToBreak = True
        else:
            self.block1.readyToBreak = False
        '''
        for row in self.block.tiles:
            for tile in row:
                delta_x = abs(((self.bomberman.rect.x + self.bomberman.rect.width // 2) // 40) - (tile.x // 40)) # вычисление разницы в координатах гг и блока
                delta_y = abs(((self.bomberman.rect.y - self.bomberman.rect.height // 2) // 40) -
                              ((tile.y - 40) // 40))
                if (delta_x <= 2 and delta_y == 0) or (delta_y <= 2 and delta_x == 0):
                    tile.readyToBreak = True
                else:
                    tile.readyToBreak = False
