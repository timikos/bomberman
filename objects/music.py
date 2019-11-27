import pygame


class Music_class:
    path_music = 'sounds/game_music.wav'
    path_explosion = 'sounds/explosion.wav'
    music = None
    explosion = None

    def __init__(self):
        if not Music_class.music and not Music_class.explosion:
            pygame.mixer.init()
            Music_class.music = pygame.mixer.Sound(Music_class.path_music)  # для возможности ссылки на объект
            Music_class.explosion = pygame.mixer.Sound(Music_class.path_explosion)  # для возможности ссылки на объект
            pygame.mixer.music.set_volume(0.001)

    # .play(loops, maxtime, fade_ms)
    # loop=-1  -> infinite playing / other values = count of repeating
    # maxtime  -> time of playing sound
    # fade_ms  -> changing sound volume with time
