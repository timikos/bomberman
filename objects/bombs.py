import pygame
from objects.base import DrawObject
from constants import BombProperties, FieldProperties
from Global import Globals


class BombFire:
    fire_filename = 'images/bombs/fire_center.png'

    def __init__(self, game, update_power=1):
        self.game = game
        self.fire_image = pygame.image.load(BombFire.fire_filename)
        self.count_fire_sides = 4
        # на сколько клеток расширим базовый огонь
        self.update_power = update_power
        self.fire_rects = []
        # если создавать массив не через цикл,
        # то скорее всего все элементы массива будут ссылками на один экземпляр pygame.Rect
        for i in range(self.count_fire_sides * self.update_power):
            self.fire_rects.append(pygame.Rect(0, 0, BombProperties.WIDTH, BombProperties.HEIGHT))

    def create_fire(self, x, y):
        for i in range(self.update_power):
            self.fire_rects[i].x = x - FieldProperties.CELL_LENGTH
            self.fire_rects[i].y = y
            self.fire_rects[i+1].x = x + FieldProperties.CELL_LENGTH
            self.fire_rects[i+1].y = y
            self.fire_rects[i+2].x = x
            self.fire_rects[i+2].y = y - FieldProperties.CELL_LENGTH
            self.fire_rects[i+3].x = x
            self.fire_rects[i+3].y = y + FieldProperties.CELL_LENGTH
        # центральный огонь
        self.fire_rects.append(pygame.Rect(x, y, BombProperties.WIDTH, BombProperties.HEIGHT))

    def show_fire(self):
        for fire_rect in self.fire_rects:
            # self.sound_explosion.play()
            self.game.screen.blit(self.fire_image, fire_rect)


class Bomb(DrawObject):
    pygame.mixer.init()
    filename = 'images/bombs/bomb.png'
    sound_explosion = pygame.mixer.Sound('sounds/explosion.wav')
    sound_explosion.set_volume(min(0.2, 0.3))

    def __init__(self, game, hidden=True):
        super().__init__(game)
        self.hidden = hidden
        self.start_ticks = 0
        self.bomb_fire = BombFire(self.game)
        self.image = pygame.image.load(Bomb.filename)
        self.rect = pygame.Rect(0, 0, FieldProperties.CELL_LENGTH, FieldProperties.CELL_LENGTH)
        self.x=0

    def create_bomb(self, x, y):
        self.x=x
        self.rect.x = x + 3
        self.rect.y = y + 3
        self.hidden = False
        self.start_ticks = pygame.time.get_ticks()

    def hide_bomb(self):
        self.hidden = True
        self.start_ticks = 0

    def process_draw(self):
        self.update_x(Globals.FieldPosition)
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if not self.hidden and seconds <= 2:
            self.game.screen.blit(self.image, self.rect)
        elif not self.hidden and 2 < seconds <= 3:
            self.bomb_fire.create_fire(self.rect.x, self.rect.y)
            self.bomb_fire.show_fire()
        elif not self.hidden and seconds > 3:
            self.hide_bomb()

    def collides_with(self, other):
        return self.rect.colliderect(other)

    def update_x(self,x):
            self.rect.x=self.x-x