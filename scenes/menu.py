"""
Сцена <Главное меню>
Класс MenuScene

Описание: данный класс реализует сцену с главным меню
"""

from constants import Color
from objects.buttons import ButtonAnimation
from scenes.base import Scene
from objects.background import Background
from Global import Globals
import pygame

class MenuScene(Scene):
    def create_objects(self):
        """Создание объектов"""
        self.button_start = ButtonAnimation(self.game, (350, 425, 100, 40), Color.WHITE, "Запуск игры",
                                            self.set_main_scene)
        self.button_info = ButtonAnimation(self.game, (350, 475, 100, 40), Color.WHITE, "Управление",
                                           self.set_info_scene)
        self.button_camera_on = ButtonAnimation(self.game, (600, 625, 140, 40), Color.WHITE, "Вкл камера v2.0",
                                             self.on_camera_status, 0)
        self.button_camera_off = ButtonAnimation(self.game, (600, 625, 140, 40), Color.WHITE, "Выкл камера v2.0",
                                                self.off_camera_status, 0)
        self.Background = Background(self.game, (0, 0))
        self.button_exit = ButtonAnimation(self.game, (350, 525, 100, 40), Color.WHITE, 'Выход', self.exit)

        """Список объектов"""
        self.objects = [self.Background, self.button_start, self.button_info, self.button_exit]

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

    def set_main_scene(self):
        """Переход на сцену игры"""
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_info_scene(self):
        """Переход на сцену с информацией"""
        self.set_next_scene(self.game.INFO_SCENE_INDEX)

    def exit(self):
        """Выход"""
        self.game.game_over = True