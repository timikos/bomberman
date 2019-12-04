"""
Класс ButtonAnimation

Описание: данный класс реализует анимированную кнопку
"""
import pygame
from constants import ButtonProperties, InterfaceProperties
from objects.base import DrawObject


class BaseButtonAnim(object):
    """Базовый класс кнопок"""
    def __init__(self, game, rect, color, function, **kwargs):
        self.game = game
        self.rect = pygame.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.basic_font = 20  # Минимальный размер текста кнопки
        self.animation = self.basic_font
        self.process_kwargs(kwargs)
        self.render_text()
        self.animation_step = 1
        self.fonts = pygame.font.Font(InterfaceProperties.TEXT_FONT, self.animation)

    def process_kwargs(self, kwargs):
        """Опции"""
        settings = {"text": None,
                    "font": pygame.font.Font(None, self.basic_font),
                    "call_on_release": True,
                    "hover_color": None,
                    "clicked_color": None,
                    "font_color": None,
                    "hover_font_color": None,
                    "clicked_font_color": None,
                    "click_sound": None,
                    "hover_sound": None}
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the buttons text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.fonts.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.fonts.render(self.text, True, color)
            self.text = self.fonts.render(self.text, True, self.font_color)

    def check_event(self, event):
        """Обработка событий"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self, surface):
        """Обновление кнопки"""
        color = self.color
        text = self.text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.animation > self.basic_font + 20:
                self.animation_step = -1
            elif self.animation <= self.basic_font:
                self.animation_step = 1
            self.animation = self.animation + self.animation_step
            if self.hover_font_color:
                text = self.hover_text
        elif self.hovered == False:
            self.animation = self.basic_font
        self.fonts = pygame.font.Font(InterfaceProperties.TEXT_FONT, self.animation)
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)


"""Анимированные кнопки"""


class ButtonAnimation(DrawObject):

    def __init__(self, game, rect=(10, 10, 100, 40), color=(0, 0, 0), text='Test', function=None):
        super().__init__(game)
        self.rect = rect
        self.color = color
        self.text = text
        self.function = function if function else ButtonAnimation.no_action
        self.internal_button = BaseButtonAnim(game, self.rect, self.color, self.function,
                                              **ButtonProperties.BUTTON_STYLE)
        self.internal_button.text = text
        self.internal_button.render_text()

    @staticmethod
    def no_action(self):
        pass

    def process_event(self, event):
        self.internal_button.check_event(event)

    def process_draw(self):
        self.internal_button.text = self.text
        self.internal_button.render_text()
        self.internal_button.update(self.game.screen)
