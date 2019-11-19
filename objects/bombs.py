import pygame
from objects.base import DrawObject


class Bomb(DrawObject):
    pygame.mixer.init()  # Звуки
    filename = 'images/bombs/bomb.png'
    fire_filename = 'images/bombs/fire.png'
    sound_explosion = pygame.mixer.Sound('sounds/explosion.wav')
    sound_explosion.set_volume(min(0.2,0.3))

    def __init__(self, game, hidden=True):
        super().__init__(game)
        self.hidden = hidden
        self.start_ticks = 0
        self.fire_image = pygame.image.load(Bomb.fire_filename)
        self.fire_rects = [pygame.Rect(0, 0, 40, 40), pygame.Rect(0, 0, 40, 40), pygame.Rect(0, 0, 40, 40), pygame.Rect(0, 0, 40, 40)]
        self.image = pygame.image.load(Bomb.filename)
        self.rect = pygame.Rect(0, 0, 40, 40)


    def create_bomb(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.fire_rects[0].x = x - 40
        self.fire_rects[0].y = y
        self.fire_rects[1].x = x + 40
        self.fire_rects[1].y = y
        self.fire_rects[2].x = x
        self.fire_rects[2].y = y - 40
        self.fire_rects[3].x = x
        self.fire_rects[3].y = y + 40
        self.hidden = False
        self.start_ticks = pygame.time.get_ticks()

    def show_fire(self):
        for i in range(len(self.fire_rects)):
            self.sound_explosion.play()
            self.game.screen.blit(self.fire_image, self.fire_rects[i])

    def hide_bomb(self):
        self.hidden = True
        self.start_ticks = 0

    def process_draw(self):
        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        print('seconds: ', seconds)
        if not self.hidden and seconds <= 2:
            self.game.screen.blit(self.image, self.rect)
        elif 2 < seconds <= 3:
            self.show_fire()
        elif seconds > 3:
            self.hide_bomb()

    def collides_with(self, other):
        return self.rect.colliderect(other)