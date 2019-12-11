"""
Сцена <Информация>
Класс InfoScene

Описание: данный класс реализует сцену с информацией для игрока
"""

from constants import Color, InterfaceProperties
from objects.background import Background
from objects.buttons import ButtonAnimation
from scenes.base import Scene
from objects.text import Text


class InfoScene(Scene):
    def create_objects(self):
        """Создание объектов"""
        self.Background = Background(self.game, (75, 75), filename="images/templates/info.jpg")
        self.text1 = Text(self.game, 280, 225, 'Управление', 55, (255, 255, 255),
                          font_name=InterfaceProperties.TEXT_FONT)
        self.text2 = Text(self.game, 280, 275, 'W - движение вверх', 25, (255, 255, 255),
                          font_name=InterfaceProperties.TEXT_FONT)
        self.text3 = Text(self.game, 280, 295, 'S - движение вниз', 25, (255, 255, 255))
        self.text4 = Text(self.game, 280, 315, 'A - движение влево', 25, (255, 255, 255))
        self.text5 = Text(self.game, 280, 335, 'D - движение вправо', 25, (255, 255, 255))
        self.text6 = Text(self.game, 280, 355, 'SPACE - поставить бомбу', 25, (255, 255, 255))
        self.button_back = ButtonAnimation(self.game, (350, 525, 100, 40), Color.WHITE, 'Назад', self.back)

        """Список объектов"""
        self.objects = [self.Background, self.button_back]

