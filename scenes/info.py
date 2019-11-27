from constants import Color, InterfaceProperties
from objects.button_animated import BtnAnim
from scenes.base import Scene
from objects.text import Text

class InfoScene(Scene):
    def create_objects(self):
        self.Text1 = Text(self.game, 280, 225, 'Управление', 55, (255, 255, 255), font_name='fonts/pixel_font.ttf')
        self.Text2 = Text(self.game, 280, 275, 'W - движение вверх', 25, (255, 255, 255), font_name=InterfaceProperties.TEXT_FONT)
        self.Text3 = Text(self.game, 280, 295, 'S - движение вниз', 25, (255, 255, 255))
        self.Text4 = Text(self.game, 280, 315, 'A - движение влево', 25, (255, 255, 255))
        self.Text5 = Text(self.game, 280, 335, 'D - движение вправо', 25, (255, 255, 255))
        self.Text6 = Text(self.game, 280, 355, 'SPACE - поставить бомбу', 25, (255, 255, 255))
        self.button_back = BtnAnim(self.game, (350, 525, 100, 40), Color.WHITE, 'Назад', self.back)
        self.objects = [self.button_back, self.Text1, self.Text2, self.Text3, self.Text4, self.Text5, self.Text6]

    def back(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)