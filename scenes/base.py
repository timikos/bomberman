"""
Класс Scene

Описание: данный класс используется как шаблон для всех классов сцен
"""
import pygame

from Global import Globals
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

    def set_lvl_1(self):
        """Загрузка 1 уровня"""
        self.current_lvl = 1
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(1)
        self.set_main_scene()
        print("Уровень 1 загружен")

    def set_lvl_2(self):
        """Загрузка 2 уровня"""
        self.current_lvl = 2
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(2)
        self.set_main_scene()
        print("Уровень 2 загружен")

    def set_lvl_3(self):
        """Загрузка 3 уровня"""
        self.current_lvl = 3
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(3)
        self.set_main_scene()
        print("Уровень 3 загружен")

    def set_lvl_4(self):
        """Загрузка 4 уровня"""
        self.current_lvl = 4
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(4)
        self.set_main_scene()
        print("Уровень 4 загружен")

    def set_lvl_5(self):
        """Загрузка 5 уровня"""
        self.current_lvl = 5
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(5)
        self.set_main_scene()
        print("Уровень 5 загружен")

    def set_main_scene(self):
        """Переход на сцену игры"""
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_info_scene(self):
        """Переход на сцену с информацией"""
        self.set_next_scene(self.game.INFO_SCENE_INDEX)

    def set_lvls_scene(self):
        """Переход на сцену с информацией"""
        self.set_next_scene(self.game.LVLS_SCENE_INDEX)

    def back(self):
        """Возвращение на сцену с главным меню"""
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def exit(self):
        """Выход"""
        self.game.game_over = True

    def on_camera_status(self):
        Globals.CameraStatus = True

    def off_camera_status(self):
        Globals.CameraStatus = False