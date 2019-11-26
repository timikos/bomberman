class Color:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 180, 0)
    YELLOW = (255, 179, 0)


class ScreenProperties:
    WIDTH = 800  # Ширина экрана
    HEIGHT = 670  # Высота экрана
    SCREEN_BORDER_WIDTH = 160  # Граница экрана по ширине
    SCREEN_BORDER_HEIGHT = 150  # Граница экрана по высоте


class FieldProperties:
    CELL_LENGTH = 40  # Длина стороны одной клетки в пикселях
    WIDTH = 31  # В клетках
    HEIGHT = 15  # В клетках


class ScoreProperties:
    HEALTH = 10  # Очков дается за оставшуюся жизнь


class BombermanProperties:
    RESPAWN_X = 400  # Появление бомбермена на оси х
    RESPAWN_Y = 320  # Появление бомбермена на оси y
    DIRECTION_X = 0  # Начальное направление
    DIRECTION_Y = 0  # Начальное направление
    WIDTH = 35  # Ширина прямоугольника бомбермена
    HEIGHT = 35  # Высота прямоугольника бомбермена


class EnemyProperties:
    WIDTH = 30  # Ширина прямоугольника врагов
    HEIGHT = 35  # Высота прямоугольника врагов
    DIRECTION_X = 0  # Начальное направление
    DIRECTION_Y = 0  # Начальное направление


class BombProperties:
    WIDTH = 30  # Ширина прямоугольника бомб
    HEIGHT = 30  # Высота прямоугольника бомб


class ScoreTableProperties:
    PLAYER_COUNT = 5
    PLAYER_NUM_WIDTH = 10  # % относительно таблицы
    NAME_WIDTH = 70  # % относительно таблицы
    SCORE_WIDTH = 20  # % относительно таблицы
    DISPLAY_HEADER = True  # Отображать заголовок таблицы
    COLOR = Color.ORANGE
    HEADER = ['N', 'Имя игрока', 'Счет']


class TableProperties:
    BACKGROUND = Color.BLACK
    FONT_FILE = 'fonts/pixel_font.ttf'
    CELL_HEIGHT = 10  # %
    WIDTH = 80  # %
    Y_SHIFT = 50  # px (отступ сверху)
    LINE_WIDTH = 2  # px
    FONT_SIZE = 40  # px
    FONT_SHIFT = 20  # px (отступ текса в ячейке относительно X)


class StatisticsProperties:
    COLOR = Color.ORANGE
    NUM_SYMBOL_WIDTH = 3  # Определяет количество ведущих нулей у числа
    NAME_WIDTH = 60  # % относительно таблицы
    NUM_WIDTH = 20  # % относительно таблицы
    ADD_SCORE_WIDTH = 20  # % относительно таблицы
    HEADER = None

class InterfaceProperties:
    TEXT_FONT = 'fonts/pixel_font.ttf'  # Шрифт
    FONT_SIZE = 40  # Размер шрифта