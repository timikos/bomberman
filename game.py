import sys
import pygame

from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.info import InfoScene
from scenes.statistics import StatisticsScene
from constants import ScreenProperties


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
        self.scenes = [MenuScene(self), MainScene(self), FinalScene(self), InfoScene(self), StatisticsScene(self)]
        self.current_scene = 0

    def create_window(self):
        pygame.init()
        pygame.mixer.music.load('sounds/game_music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def main_loop(self):
        while not self.game_over:
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.game_over = True
            self.scenes[self.current_scene].process_frame(eventlist)
        sys.exit(0)
