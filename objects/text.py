import pygame

from objects.base import DrawObject


class Text(DrawObject):
    def __init__(self, game, x=100, y=100, text='Define me!', font_size=35, color=(255, 255, 255),
                 font_name='Comic Sans', is_bold=True, is_italic=False):
        super().__init__(game)
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.is_bold, self.is_italic)
        self.update_text(text)

    def update_font(self, font_size, font_name, is_bold, is_italic):
        self.font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)

    def update_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)

    def process_draw(self):
        self.game.screen.blit(self.text_surface, [self.x, self.y])