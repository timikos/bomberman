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
        self.font = pygame.font.Font('fonts/pixel_font.ttf', self.size)
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

    def write_to_file(self, file_path='score.txt', name='Player'):
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
        HighScoreTable.need_to_update()



class HighScoreTable(DrawObject):
    PLAYER_COUNT = 5
    WIDTH = 80  # %
    CELL_HEIGHT = 10  # %
    PLAYER_NUM_WIDTH = 10  # % относительно таблицы
    NAME_WIDTH = 70  # % относительно таблицы
    SCORE_WIDTH = 20  # % относительно таблицы
    Y_SHIFT = 50  # px (отступ сверху)
    LINE_WIDTH = 2  # px
    FONT_SIZE = 40  # px
    FONT_SHIFT = 20  # px (отступ текса в ячейке относительно X)
    DISPLAY_HEADER = True  # Отображать заголовок таблицы
    COLOR = Color.ORANGE
    HEADER = ['N', 'Имя игрока', 'Счет']
    info_updated = False

    @staticmethod
    def str_to_text(s, bold=False):
        return pygame.font.Font(None, HighScoreTable.FONT_SIZE, bold=bold).render(str(s), 1, HighScoreTable.COLOR)

    @staticmethod
    def parse_file(file_path='score.txt'):
        players = []
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    if line != '\n' and line != '':
                        player, score = line.split('=>')
                        score = int(score)
                        players += [{'name': player, 'score': score}]
            players.sort(key=lambda x: x['score'], reverse=True)
            return players[:HighScoreTable.PLAYER_COUNT]
        return []

    @staticmethod
    def need_to_update():
        HighScoreTable.info_updated = False

    def __init__(self, game, file_path='score.txt'):
        self.file_path = file_path
        self.cells = [self.PLAYER_NUM_WIDTH, self.NAME_WIDTH, self.SCORE_WIDTH]
        self.texts = []
        super().__init__(game)

    def update_info(self):
        self.texts = []
        if self.DISPLAY_HEADER:
            self.texts += [[]]
            for i in self.HEADER:
                text = self.str_to_text(i, bold=False)
                self.texts[0] += [text]
        players = self.parse_file(self.file_path)
        for i in range(len(players)):
            self.texts += [[]]
            self.texts[-1] += [self.str_to_text(i + 1)]
            self.texts[-1] += [self.str_to_text(players[i]['name'])]
            self.texts[-1] += [self.str_to_text(players[i]['score'])]
        HighScoreTable.info_updated = True

    def get_width(self):
        return int(self.game.width * self.WIDTH / 100)

    def get_x(self):
        return self.game.width // 2 - self.get_width() // 2

    def get_y(self):
        return self.Y_SHIFT

    def get_pos(self):
        return self.get_x(), self.get_y()

    def get_cell_height(self):
        return int(self.game.height * self.CELL_HEIGHT / 100)

    def set_text_to_cell(self, n, m, text):
        x = self.get_x() + self.get_width() * sum(self.cells[:m]) // 100 + self.FONT_SHIFT
        y = self.get_y() + n * self.get_cell_height() + (self.get_cell_height() - text.get_height()) // 2
        self.game.screen.blit(text, (x, y))

    def process_draw(self):
        if not self.info_updated:
            self.update_info()
        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_cell_height() * (self.PLAYER_COUNT + int(self.DISPLAY_HEADER))
        pygame.draw.rect(self.game.screen, Color.BLACK, pygame.Rect((x, y), (width, height)))
        for i in range(self.PLAYER_COUNT + 1 + int(self.DISPLAY_HEADER)):
            pygame.draw.line(self.game.screen, self.COLOR, (x, y + self.get_cell_height() * i),
                             (x + self.get_width(), y + self.get_cell_height() * i), self.LINE_WIDTH)
        for i in range(4):
            y1 = y
            y2 = y + self.get_cell_height() * (self.PLAYER_COUNT + int(self.DISPLAY_HEADER))
            x1 = x2 = int(x + width * sum(self.cells[:i]) / 100)
            pygame.draw.line(self.game.screen, self.COLOR, (x1, y1), (x2, y2), self.LINE_WIDTH)
        for i in range(len(self.texts)):
            for j in range(len(self.texts[i])):
                self.set_text_to_cell(i, j, self.texts[i][j])

