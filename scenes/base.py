"""
Класс Scene

Описание: данный класс используется как шаблон для всех классов сцен
"""
import pygame
from constants import Color



class Scene:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.objects = []  # Объекты, который будут на сцене
        self.create_objects()  # Создание объектов

    def create_objects(self):
        pass

    def process_frame(self, eventlist):
        """Обработка всех событий, всей логики, всей отрисовки"""
        self.process_all_events(eventlist)
        self.process_all_logic()
        self.process_all_draw()


    def process_all_events(self, eventlist):
        """Обработка всех событий"""
        for event in eventlist:
            self.process_current_event(event)

    def process_current_event(self, event):
        """Обработка конкретного события"""
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def additional_event_check(self, event):
        pass

    def process_all_logic(self):
        """Обработка всей логики"""
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def additional_logic(self):
        pass

    def process_all_draw(self):
        """Обработка всей отрисовки"""
        self.screen.fill(Color.BLACK)
        for item in self.objects:
            item.process_draw()
        self.additional_draw()
        pygame.display.flip()  # Переворот экрана
        pygame.time.wait(10)  # Ожидание в 10 милисекунд

    def additional_draw(self):
        pass

    def set_next_scene(self, index):
        """Присваевание индекса данной сцене"""
        self.game.current_scene = index
