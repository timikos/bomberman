"""
Сцена <Выбор уровня>
Класс LvlsScene

Описание: данный класс реализует сцену с выбором уровня
"""

from constants import Color
from objects.buttons import ButtonAnimation
from scenes.base import Scene
from objects.background import Background
from Global import Globals
import pygame


class LvlsScene(Scene):
    current_lvl = 1  # Текущий уровень
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
        self.button_camera_on = ButtonAnimation(self.game, (600, 625, 140, 40), Color.WHITE, "Вкл камера v2.0",
                                                self.on_camera_status, 0)
        self.button_camera_off = ButtonAnimation(self.game, (600, 625, 140, 40), Color.WHITE, "Выкл камера v2.0",
                                                 self.off_camera_status, 0)
        self.button_back = ButtonAnimation(self.game, (350, 560, 100, 40), Color.WHITE, 'Назад', self.back)
        self.button_exit = ButtonAnimation(self.game, (350, 600, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.Background = Background(self.game, (0, 0))

        """Список объектов"""
        self.objects = [self.Background, self.button_exit, self.button_back,
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
