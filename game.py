"""
Класс Game

Описание: данный класс соединяет в себе все сцены, все найстройки
"""
import sys
import pygame
from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.info import InfoScene
from scenes.statistics import StatisticsScene
from constants import ScreenProperties
from objects.music import Sound


class Game:
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    INFO_SCENE_INDEX = 3
    STATISTICS_SCENE_INDEX = 4

    def __init__(self, width=ScreenProperties.WIDTH, height=ScreenProperties.HEIGHT):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.create_window()
        self.game_over = False
        self.wall_collision_count = 0
        self.ticks = 0
        self.current_scene = 0
        self.previus_scene = self.current_scene

        self.scenes = [  # Список сцен
            MenuScene(self),
            MainScene(self),
            FinalScene(self),
            InfoScene(self),
            StatisticsScene(self)
        ]

    def create_window(self):
        pygame.init()  # Инициализация pygame
        pygame.display.set_caption("Bomberman")  # Название игры в шапке
        pygame.display.set_icon(pygame.image.load("images/icon.png"))  # Иконка в шапке
        self.music = Sound()  # Звуковое обеспечение

        # Экран камеры
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def main_loop(self):
        """Главный цикл игры"""
        while not self.game_over:
            eventlist = pygame.event.get()  # Получение события
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.game_over = True
            if self.current_scene != self.previus_scene and self.current_scene==1:
                self.scenes[self.current_scene].process_all_draw('all')
                self.previus_scene = self.current_scene
            self.scenes[self.current_scene].process_frame(eventlist)  # Обработка текущей сцены
        sys.exit(0)
