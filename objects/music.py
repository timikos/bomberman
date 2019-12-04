"""
Класс Sound

Описание: данный класс позволяет редактировать звуковое обеспечение
"""

import pygame


class Sound:
    """Звуки"""
    path_music = 'sounds/game_music.ogg'
    path_explosion = 'sounds/explosion.wav'
    music = None
    explosion = None

    def __init__(self):
        if not Sound.music and not Sound.explosion:
            pygame.mixer.init()
            Sound.music = pygame.mixer.Sound(Sound.path_music)  # Музыка на фоне
            Sound.explosion = pygame.mixer.Sound(Sound.path_explosion)  # Звук взрыва бомбы
            Sound.music.play(-1)
            Sound.music.set_volume(0.1)  # Громкость музыки
            Sound.explosion.set_volume(0.3)  # Громкость взрыва
