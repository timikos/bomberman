import pygame
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
        self.rect = pygame.Rect(self.x, self.y, 0, 0)
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


class TileMap(DrawObject):

    def __init__(self, game, x=0, y=0, width=FieldProperties.WIDTH, height=FieldProperties.HEIGHT):
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

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.x = x
        self.y = y
        self.isDestroyed = False
        self.image = pygame.image.load(DestroyedBlock.filename)

    def process_draw(self):
        if not self.isDestroyed:
            self.game.screen.blit(self.image, self.rect)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == ' ':  # space bar is pressed
                print('APC')
                DestroyedBlock.explosion_event = pygame.USEREVENT + 1
                pygame.time.set_timer(DestroyedBlock.explosion_event, 2000)

        if event.type == DestroyedBlock.explosion_event:
            DestroyedBlock.explosion_event = None
            self.isDestroyed = True
            print('boom')