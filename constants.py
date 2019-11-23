class Color:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    ORANGE = (255, 180, 0)
    YELLOW = (255, 179, 0)

class ScreenProperties:
    WIDTH = 800 # Ширина экрана
    HEIGHT = 670 # Высота экрана
    SCREEN_BORDER_WIDTH = 160  # Граница экрана по ширине
    SCREEN_BORDER_HEIGHT = 150 # Граница экрана по высоте

class FieldProperties:
    CELL_LENGTH = 40  # Длина стороны одной клетки в пикселях
    WIDTH = 31  # В клетках
    HEIGHT = 15  # В клетках

class BombermanProperties:
    RESPAWN_X = 400 # Появление бомбермена на оси х
    RESPAWN_Y = 300 # Появление бомбермена на оси y
    DIRECTION_X = 0 # Начальное направление
    DIRECTION_Y = 0 # Начальное направление
    WIDTH = 35 # Ширина прямоугольника бомбермена
    HEIGHT = 40 # Высота прямоугольника бомбермена

class EnemyProperties:
    WIDTH = 30  # Ширина прямоугольника врагов
    HEIGHT = 35  # Высота прямоугольника врагов
    DIRECTION_X = 0  # Начальное направление
    DIRECTION_Y = 0  # Начальное направление

class BombProperties:
    WIDTH = 30  # Ширина прямоугольника бомб
    HEIGHT = 30  # Высота прямоугольника бомб