"""
Сцена <Главное меню>
Класс MenuScene

Описание: данный класс реализует сцену с главным меню
"""
import json

from constants import Color
from objects.buttons import ButtonAnimation
from scenes.base import Scene
from objects.background import Background
from Global import Globals
import pygame


class LvlsScene(Scene):
    cur = 1
    def create_objects(self):
        """Создание объектов"""
        self.button_1_lvl = ButtonAnimation(self.game, (350, 400, 100, 40), Color.WHITE, "1 - Поляна",
                                            self.set_lvl_1)
        self.button_2_lvl = ButtonAnimation(self.game, (350, 430, 100, 40), Color.WHITE, "2 - Пустыня",
                                            self.set_lvl_2)
        self.button_3_lvl = ButtonAnimation(self.game, (350, 460, 100, 40), Color.WHITE, "3 - Зима",
                                            self.set_lvl_3)
        self.button_4_lvl = ButtonAnimation(self.game, (350, 490, 100, 40), Color.WHITE, "4 - Гора",
                                            self.set_lvl_4)
        self.button_5_lvl = ButtonAnimation(self.game, (350, 520, 100, 40), Color.WHITE, "5 - Ад",
                                            self.set_lvl_5)
        self.button_exit = ButtonAnimation(self.game, (350, 575, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.button_camera_on = ButtonAnimation(self.game, (600, 625, 140, 40), Color.WHITE, "Вкл камера v2.0",
                                                self.on_camera_status, 0)
        self.button_camera_off = ButtonAnimation(self.game, (600, 625, 140, 40), Color.WHITE, "Выкл камера v2.0",
                                                 self.off_camera_status, 0)

        self.Background = Background(self.game, (0, 0))

        """Список объектов"""
        self.objects = [self.Background, self.button_exit,
                        self.button_1_lvl, self.button_2_lvl, self.button_3_lvl, self.button_4_lvl, self.button_5_lvl]

    def process_all_draw(self):
        """Обработка всей отрисовки"""
        self.screen.fill(Color.BLACK)
        for item in self.objects:
            item.process_draw()
        if Globals.CameraStatus is False:
            self.button_camera_on.process_draw()
        else:
            self.button_camera_off.process_draw()
        self.additional_draw()
        pygame.display.flip()  # Переворот экрана
        pygame.time.wait(10)

    def process_all_logic(self):
        """Обработка всей логики"""
        for item in self.objects:
            item.process_logic()
        if Globals.CameraStatus is False:
            self.button_camera_on.process_logic()
        else:
            self.button_camera_off.process_logic()
        self.additional_logic()

    def process_current_event(self, event):
        """Обработка конкретного события"""
        for item in self.objects:
            item.process_event(event)
        if Globals.CameraStatus is False:
            self.button_camera_on.process_event(event)
        else:
            self.button_camera_off.process_event(event)
        self.additional_event_check(event)

    def on_camera_status(self):
        Globals.CameraStatus = True

    def off_camera_status(self):
        Globals.CameraStatus = False

    def set_lvl_1(self):
        self.cur = 1
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(1)
        self.set_main_scene()

    def set_lvl_2(self):
        self.cur = 2
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(2)
        self.set_main_scene()

    def set_lvl_3(self):
        self.cur = 3
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(3)
        self.set_main_scene()

    def set_lvl_4(self):
        self.cur = 4
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(4)
        self.set_main_scene()

    def set_lvl_5(self):
        self.cur = 5
        self.game.scenes[self.game.MAIN_SCENE_INDEX].load_level(5)
        self.set_main_scene()

    def set_main_scene(self):
        """Переход на сцену игры"""
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)


    def exit(self):
        """Выход"""
        self.game.game_over = True