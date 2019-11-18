from third_party.buttons.button_animated import ButtonAnim
from constants import Color
from objects.base import DrawObject


class BtnAnim(DrawObject):
    BUTTON_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.YELLOW,
        "clicked_color": Color.GREEN,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE
    }

    def __init__(self, game, geometry=(10, 10, 100, 40), color=(0, 0, 0), text='Test', function=None):
        super().__init__(game)
        self.geometry = geometry
        self.color = color
        self.text=text
        self.function = function if function else BtnAnim.no_action
        self.internal_button = ButtonAnim(game, self.geometry, self.color, self.function, **BtnAnim.BUTTON_STYLE)
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