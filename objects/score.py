"""
Классы Score, Table, StatisticsTable, HighScoreTable

Описание: данные классы реализуют вывод на экран количество очков,
таблицу общего счёта и лучший счёт, а так же
производит запись в файл
"""
import pygame
from objects.base import DrawObject
from constants import Color, ScoreTableProperties, TableProperties, StatisticsProperties, InterfaceProperties, ScorePosition
import os


class Score(DrawObject):
    """Счёт во время игры"""
    def __init__(self, game, color=Color.ORANGE, count=0, size=InterfaceProperties.FONT_SIZE,
                 pos=ScorePosition.RIGHT_BOTTOM, text_before="SCORE: ",
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
        """Получение текста"""
        return self.text_before + str(self.count) + self.text_after

    def get_width(self):
        """Получение ширины текста"""
        return self.text.get_width()

    def get_height(self):
        """Получение высоты текста"""
        return self.text.get_height()

    def get_count(self):
        """Получение значение"""
        return self.count

    def set_count(self, count):
        """Задать значение"""
        self.count = count
        self.update()

    def add_count(self, delta):
        """Добавить значение"""
        self.count += delta
        self.update()

    def sub_count(self, delta):
        """Вычесть значение"""
        self.count -= delta
        if self.count < 0:
            self.count = 0
        self.update()

    def update(self):
        """Обновление текста"""
        self.font = pygame.font.Font(InterfaceProperties.TEXT_FONT, InterfaceProperties.FONT_SIZE)
        self.text = self.font.render(self.get_text(), 1, self.color)

    def set_and_get_position(self):
        """Назначение и получение координат"""
        if self.pos == ScorePosition.LEFT_TOP:
            x = self.border_shift[0]
            y = self.border_shift[1]
        elif self.pos == ScorePosition.CENTER_TOP:
            x = self.game.width // 2 - self.get_width() // 2
            y = self.border_shift[1]
        elif self.pos == ScorePosition.RIGHT_TOP:
            x = self.game.width - self.get_width() - self.border_shift[0]
            y = self.border_shift[1]
        elif self.pos == ScorePosition.LEFT_BOTTOM:
            x = self.border_shift[1]
            y = self.game.height - self.get_height() - self.border_shift[1]
        elif self.pos == ScorePosition.CENTER_BOTTOM:
            x = self.game.width // 2 - self.get_width() // 2
            y = self.game.height - self.get_height() - self.border_shift[1]
        elif self.pos == ScorePosition.RIGHT_BOTTOM:
            x = self.game.width - self.get_width() - self.border_shift[0]
            y = self.game.height - self.get_height() - self.border_shift[1]
        else:
            x, y = self.border_shift[0], self.border_shift[1]
        return x, y

    def process_draw(self):
        self.game.screen.blit(self.text, self.set_and_get_position())


"""Счёт в конце игры"""
class Table(DrawObject):
    def __init__(self, game, color, cells, data, header=None, display_border=True):
        self.color = color
        self.cells = cells  # Представляет собой массив из чисел, где каждое число - ширина клетки в процентах
        self.header = header  # Массив из строк
        self.data = []  # Двумерный массив
        self.texts = []
        self.display_border = display_border
        self.update_data(data)
        super().__init__(game)

    def update_data(self, data):
        """Обновление значений в массиве счёта"""
        self.data = data
        self.texts = []
        if self.header is not None:
            self.texts += [[]]
            for i in self.header:
                text = self.str_to_text(i)
                self.texts[0] += [text]
        for i in data:
            self.texts += [[]]
            for j in i:
                self.texts[-1] += [self.str_to_text(j)]

    def str_to_text(self, s):
        """Рендер строки счёта"""
        return pygame.font.Font(TableProperties.FONT_FILE, TableProperties.FONT_SIZE).render(
            str(s), 1,
            self.color)

    def get_width(self):
        """Получение ширины"""
        return int(self.game.width * TableProperties.WIDTH / 100)

    def get_x(self):
        """Получение позиции по оси Х"""
        return self.game.width // 2 - self.get_width() // 2

    @staticmethod
    def get_y():
        """Получение позиции по оси Y"""
        return TableProperties.Y_SHIFT

    def get_pos(self):
        """Получение координат"""
        return self.get_x(), self.get_y()

    def get_cell_height(self):
        """Получение высоты клетки"""
        return int(self.game.height * TableProperties.CELL_HEIGHT / 100)

    def set_text_to_cell(self, n, m, text):
        x = self.get_x() + self.get_width() * sum(self.cells[:m]) // 100 + TableProperties.FONT_SHIFT
        y = self.get_y() + n * self.get_cell_height() + (self.get_cell_height() - text.get_height()) // 2
        self.game.screen.blit(text, (x, y))

    def process_draw(self):
        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_cell_height() * (len(self.data) + int(self.header is not None))
        pygame.draw.rect(self.game.screen, Color.BLACK, pygame.Rect((x, y), (width, height)))
        for i in range(len(self.data) + 1 + int(self.header is not None)):
            if self.display_border:
                pygame.draw.line(self.game.screen, self.color, (x, y + self.get_cell_height() * i),
                                 (x + self.get_width(), y + self.get_cell_height() * i), TableProperties.LINE_WIDTH)
        for i in range(4):
            y1 = y
            y2 = y + self.get_cell_height() * (len(self.data) +
                                               int(self.header is not None))
            x1 = x2 = int(x + width * sum(self.cells[:i]) / 100)
            if self.display_border:
                pygame.draw.line(self.game.screen, ScoreTableProperties.COLOR, (x1, y1), (x2, y2),
                                 TableProperties.LINE_WIDTH)
        for i in range(len(self.texts)):
            for j in range(len(self.texts[i])):
                self.set_text_to_cell(i, j, self.texts[i][j])


"""Таблица статистики общего счёта"""
class StatisticsTable(Table):
    file_path = 'score.txt'

    def __init__(self, game, info=None):
        super().__init__(game, StatisticsProperties.COLOR,
                         [StatisticsProperties.NAME_WIDTH, StatisticsProperties.NUM_WIDTH], [],
                         StatisticsProperties.HEADER, False)
        self.info = info if info is not None else []  # Массив структуры [[name, num] * n]
        self.set_info(info)
        self.start_time = pygame.time.get_ticks()
        self.file_path = StatisticsTable.file_path

    def set_info(self, info, write_to_file=False):
        self.info = info
        self.start_time = pygame.time.get_ticks()
        if write_to_file:
            self.write_to_file()

    def write_to_file(self, name='Player'):
        """Запись в файл"""
        count = sum([i[2] for i in self.info])
        players = {}
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                for line in f.readlines():
                    if line != '\n' and line != '':
                        player, score = line.split('=>')
                        score = int(score)
                        if player not in players.keys() or players[player] < score:
                            players[player] = score
        if name not in players.keys() or players[name] < count:
            players[name] = count
        players = sorted(players.items(), key=lambda x: x[1], reverse=True)
        with open(self.file_path, 'w') as f:
            for p in players:
                f.write(p[0] + '=>' + str(p[1]) + '\n')
        HighScoreTable.need_to_update()

    def process_logic(self):
        """Обработка логики"""
        t = (pygame.time.get_ticks() - self.start_time)
        data = []
        score = 0
        format_str = '{0:0>' + str(StatisticsProperties.NUM_SYMBOL_WIDTH) + '}'
        for ind in range(len(self.info)):
            i = self.info[ind]
            to_add = i[2] // StatisticsProperties.TIME_TO_SHOW
            if to_add == 0:
                to_add = 1
            if t * to_add >= i[2]:
                data += [[i[0], format_str.format(i[1]), '+' + format_str.format(i[2])]]
                score += i[2]
            elif t != 0:
                data += [[i[0], format_str.format(i[1]), '+' + format_str.format(t * to_add)]]
                score += t * to_add
            else:
                data += [[''] * 3]
            t -= StatisticsProperties.TIME_TO_SHOW
            if t < 0:
                t = 0
        data += [['Общий счет', '', score]]
        self.update_data(data)


"""Таблица лучшего счёта"""
class HighScoreTable(Table):
    info_updated = False
    file_path = 'score.txt'

    def __init__(self, game, file_path):
        self.file_path = HighScoreTable.file_path
        self.texts = []
        super().__init__(game, ScoreTableProperties.COLOR,
                         [ScoreTableProperties.PLAYER_NUM_WIDTH,
                          ScoreTableProperties.NAME_WIDTH,
                          ScoreTableProperties.SCORE_WIDTH], self.get_players_info(),
                         (ScoreTableProperties.HEADER if ScoreTableProperties.DISPLAY_HEADER else None))

    @staticmethod
    def parse_file():
        players = []
        if os.path.isfile(HighScoreTable.file_path):
            with open(HighScoreTable.file_path, 'r') as f:
                for line in f.readlines():
                    if line != '\n' and line != '':
                        player, score = line.split('=>')
                        score = int(score)
                        players += [{'name': player, 'score': score}]
            players.sort(key=lambda x: x['score'], reverse=True)
            return players[:ScoreTableProperties.PLAYER_COUNT]
        return []

    def get_players_info(self):
        """Получение информации о счёте игрока"""
        players = self.parse_file()
        return [(i + 1, players[i]['name'], players[i]['score']) for i in range(len(players))]

    @staticmethod
    def need_to_update():
        """Нужно ли обновить"""
        HighScoreTable.info_updated = False


    def update_info(self):
        """Обновление информации"""
        self.update_data(self.get_players_info())
        self.info_updated = True

    def process_logic(self):
        """Обработка логики"""
        if not self.info_updated:
            self.update_info()
