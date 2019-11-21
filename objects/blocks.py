import pygame
from random import randint
from constants import FieldProperties
from objects.base import DrawObject


class Block(DrawObject):

    def __init__(self, game, x=0, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.border = []
        self.x = x
        self.y = y
        self.width = width  # Ширина поля в клетках
        self.height = height  # Высота поля в клетках
        self.rect = pygame.Rect(self.x, self.y, 35, 25)
        self.isDestructed = False


class IndestructibleBlock(Block):
    filename = 'images/blocks/block.png'

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.x = x
        self.y = y
        self.image = pygame.image.load(IndestructibleBlock.filename)

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def process_event(self, event):
        pass

    def collides_with(self, other):
        return self.rect.colliderect(other)



class TileMap(DrawObject):

    def __init__(self, game, x=40, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.x = x
        self.y = y
        self.tiles = []
        for x in range(width):
            self.tiles += [[]]
            for y in range(height):
                if (x == 0 or x == width - 1 or y == 0 or y == height - 1) \
                        or ((x + 1) % 2 != 0 and (y + 1) % 2 != 0):
                    self.tiles[-1].append(IndestructibleBlock(game, self.x + FieldProperties.CELL_LENGTH * x,
                                                              self.y + FieldProperties.CELL_LENGTH * y))

    def process_draw(self):
        for x in self.tiles:
            for tile in x:
                tile.process_draw()

    def process_event(self, event):
        for x in self.tiles:
            for tile in x:
                tile.process_event(event)


class DestroyedBlock(Block):
    filename = 'images/blocks/d_block_0.png'
    explosion_event = pygame.USEREVENT + 1

    def __init__(self, game, x=3, y=4):
        super().__init__(game, x * 40, y * 40)
        self.x = x * 40
        self.y = y * 40
        self.readyToBreak = False
        self.isDestroyed = False
        self.image = pygame.image.load(DestroyedBlock.filename)

    def process_draw(self):
        if not self.isDestroyed:
            self.game.screen.blit(self.image, self.rect)

    def process_event(self, event):
        pass
        #if event.type == pygame.KEYDOWN:
        #    if chr(event.key) == ' ':  # space bar is pressed
        #        DestroyedBlock.explosion_event = pygame.USEREVENT + 1
        #        pygame.time.set_timer(DestroyedBlock.explosion_event, 2000)  # задержка в две секунды

        #if self.readyToBreak:
        #    if event.type == DestroyedBlock.explosion_event:
        #        DestroyedBlock.explosion_event = None
        #        self.isDestroyed = True

    def collides_with(self, other):
        if not self.isDestroyed:
            return self.rect.colliderect(other)
        else:
            return False


class DestroyableTileMap(DrawObject):

    def __init__(self, game, x=0, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
        super().__init__(game)
        self.x = x
        self.y = y
        self.tiles = []
        for x in range(width):
            self.tiles += [[]]
            for y in range(height):
                if not (x == 0 or x == width - 1 or y == 0 or y == height - 1) \
                        and not ((x + 1) % 2 != 0 and (y + 1) % 2 != 0) and (randint(0, 170)//100):
                    self.tiles[-1].append(DestroyedBlock(game, self.x + x + 1, self.y + y))

    def process_draw(self):
        for x in self.tiles:
            for tile in x:
                tile.process_draw()

    def process_event(self, event):
        for x in self.tiles:
            for tile in x:
                tile.process_event(event)


