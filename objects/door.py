import pygame

from objects.base import DrawObject

class Door(DrawObject):
    filename = 'images/door/door.png'

    def __init__(self, game, hidden=True, x=80, y=80):
        super().__init__(game)
        self.image = pygame.image.load(Door.filename)
        self.hidden = hidden
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        #self.rect = self.image.get_rect()  # rect необходим для коллизии игрока с дверью
        #self.rect.x = 120
        #self.rect.y = 400


    def collides_with(self, bomberman):
        """Персонаж должен зайти в дверь для завершения уровня"""
        return self.rect.colliderect(bomberman)


    def show_door(self):
        self.hidden = False

    def process_logic(self):
        pass

    def process_draw(self):
        """Метод появления двери. Дверь появляется при условии, что все призраки убиты."""
        # Дверь не должна появляться на месте неразрушаемых блоков
        # Добавить импорт ghosts

        if not self.hidden:
            self.game.screen.blit(self.image, self.rect)
