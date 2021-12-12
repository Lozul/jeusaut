import pyxel

from jeusaut.object import Object


class Button(Object):
    def __init__(self, x, y, text, command):
        Object.__init__(self, x, y, len(text) * 4, 5)

        self.text = text
        self.command = command

    @property
    def hovered(self):
        return super().is_colliding_xy(pyxel.mouse_x, pyxel.mouse_y)

    def update(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.hovered:
            self.command()

    def draw(self):
        pyxel.text(self.x, self.y, self.text, 7)

        if self.hovered:
            pyxel.rectb(self.x - 2, self.y - 2, self.width + 3, self.height + 4, 7)