import pygame
from random import randint
from constants import FieldProperties
from objects.base import DrawObject


class Block(DrawObject):
    def __init__(self, game, x=0, y=0, cell_length=FieldProperties.CELL_LENGTH):
        super().__init__(game)
        self.border = []
        self.x = x * cell_length
        self.y = y * cell_length
        self.cell_length = cell_length
        self.rect = pygame.Rect(self.x, self.y, cell_length, 35)


class IndestructibleBlock(Block):
    filename = 'images/blocks/block.png'

    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.x = x * self.cell_length
        self.y = y * self.cell_length
        self.image = pygame.image.load(IndestructibleBlock.filename)

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def process_event(self, event):
        pass

    def collides_with(self, other):
        return self.rect.colliderect(other)


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
                    self.tiles[-1].append(IndestructibleBlock(game, self.x + x + 1, self.y + y))

    def process_draw(self):
        for x in self.tiles:
            for tile in x:
                tile.process_draw()

    def process_event(self, event):
        for x in self.tiles:
            for tile in x:
                tile.process_event(event)


class DestroyedBlock(Block):
    dblock_image = []
    for i in range(6):
        dblock_image.append('images/blocks/d_block_{}.png'.format(i))

    explosion_event = pygame.USEREVENT + 1

    def __init__(self, game, x=0, y=0):
        super().__init__(game, x, y)
        self.x = x * self.cell_length
        self.y = y * self.cell_length
        self.destruction_time = 5
        self.readyToBreak = False
        self.isDestroyed = False
        self.image = pygame.image.load(DestroyedBlock.dblock_image[0])
        self.start_ticks = 0

    def destruction(self):
        milsec = (pygame.time.get_ticks() - self.start_ticks) // (self.destruction_time * 20) + 1
        self.image = pygame.image.load(DestroyedBlock.dblock_image[milsec])
        self.game.screen.blit(self.image, self.rect)
        return milsec

    def process_draw(self):
        if not self.isDestroyed:
            self.game.screen.blit(self.image, self.rect)
            if self.readyToBreak:
                if self.destruction() >= self.destruction_time:
                    self.isDestroyed = True

    def process_event(self, event):
        pass
        # if event.type == pygame.KEYDOWN:
        #    if chr(event.key) == ' ':  # space bar is pressed
        #        DestroyedBlock.explosion_event = pygame.USEREVENT + 1
        #        pygame.time.set_timer(DestroyedBlock.explosion_event, 2000)  # задержка в две секунды

        # if self.readyToBreak:
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
                        and not ((x + 1) % 2 != 0 and (y + 1) % 2 != 0) and (randint(0, 170) // 100):
                    self.tiles[-1].append(DestroyedBlock(game, self.x + x + 1, self.y + y))


    def process_draw(self):
        for x in self.tiles:
            for tile in x:
                tile.process_draw()

    def process_event(self, event):
        for x in self.tiles:
            for tile in x:
                tile.process_event(event)
