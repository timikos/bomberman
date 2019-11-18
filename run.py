import sys

import pygame
from game import Game
from objects.field import Field
from constants import FieldProperties
from objects.bomberman import Bomberman

if __name__ == '__main__':
    g = Game()
    g.main_loop()
