"""
Класс DrawObject

Описание: данный класс используется как шаблон для всех наследуемых классов объектов
"""
class DrawObject:
    def __init__(self, game):
        self.game = game

    def process_event(self, event):
        """Обработка событий"""
        pass

    def process_logic(self):
        """Обработка логики"""
        pass

    def process_draw(self):
        """Отрисовка"""
        pass
