import pygame
from enum import Enum
from objects.base import DrawObject
from constants import Color
import os


class ScorePos(Enum):
    LEFT_TOP = 0
    CENTER_TOP = 1
    RIGHT_TOP = 2
    LEFT_BOTTOM = 3
    CENTER_BOTTOM = 4
    RIGHT_BOTTOM = 5


class Score(DrawObject):
    def __init__(self, game, color=Color.ORANGE, count=0, size=60, pos=ScorePos.RIGHT_BOTTOM, text_before="SCORE: ",
                 text_after="", border_shift=(10, 10)):
        self.color = color
        self.border_shift = border_shift  # Сдвиг надписи от края
        self.count = count
        self.size = size
        self.pos = pos
        self.text_before = text_before
        self.text_after = text_after
        self.font = None
        self.text = None
        self.update()
        super().__init__(game)

    def get_text(self):
        return self.text_before + str(self.count) + self.text_after

    def get_width(self):
        return self.text.get_width()

    def get_height(self):
        return self.text.get_height()

    def get(self):
        return self.count

    def set(self, count):
        self.count = count
        self.update()

    def add(self, delta):
        self.count += delta
        self.update()

    def sub(self, delta):
        self.count -= delta
        if self.count < 0:
            self.count = 0
        self.update()

    def update(self):
        self.font = pygame.font.Font(None, self.size)
        self.text = self.font.render(self.get_text(), 1, self.color)

    def get_coordinates(self):
        if self.pos == ScorePos.LEFT_TOP:
            x = self.border_shift[0]
            y = self.border_shift[1]
        elif self.pos == ScorePos.CENTER_TOP:
            x = self.game.width // 2 - self.get_width() // 2
            y = self.border_shift[1]
        elif self.pos == ScorePos.RIGHT_TOP:
            x = self.game.width - self.get_width() - self.border_shift[0]
            y = self.border_shift[1]
        elif self.pos == ScorePos.LEFT_BOTTOM:
            x = self.border_shift[1]
            y = self.game.height - self.get_height() - self.border_shift[1]
        elif self.pos == ScorePos.CENTER_BOTTOM:
            x = self.game.width // 2 - self.get_width() // 2
            y = self.game.height - self.get_height() - self.border_shift[1]
        elif self.pos == ScorePos.RIGHT_BOTTOM:
            x = self.game.width - self.get_width() - self.border_shift[0]
            y = self.game.height - self.get_height() - self.border_shift[1]
        else:
            x, y = self.border_shift[0], self.border_shift[1]
        return x, y

    def process_draw(self):
        self.game.screen.blit(self.text, self.get_coordinates())

    def write_to_file(self, file_path, name):
        players = {}
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    if line != '\n' and line != '':
                        player, score = line.split('=>')
                        score = int(score)
                        if player not in players.keys() or players[player] < score:
                            players[player] = score
        if name not in players.keys() or players[name] < self.count:
            players[name] = self.count
        players = sorted(players.items(), key=lambda x: x[1], reverse=True)
        with open(file_path, 'w') as f:
            for p in players:
                f.write(p[0] + '=>' + str(p[1]) + '\n')
