import pygame


class Music_class:
    pygame.mixer.init()

    # path_music = 'sounds/game_music.wav'
    # path_explosion = 'sounds/explosion.wav'

    music = pygame.mixer.Sound('sounds/game_music.wav')  # для возможности ссылки на объект
    explosion = pygame.mixer.Sound('sounds/explosion.wav')  # для возможности ссылки на объект

    pygame.mixer.music.set_volume(0.05)

    # .play(loops, maxtime, fade_ms)
    # loop=-1  -> infinite playing / other values = count of repeating
    # maxtime  -> time of playing sound
    # fade_ms  -> changing sound volume with time
