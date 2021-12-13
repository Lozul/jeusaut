import pyxel

from jeusaut.object import Object


class Text(Object):

    color = 7

    def __init__(self, x, y, text, **kwargs):
        Object.__init__(self, x, y, len(text) * 4, 5)

        self.text = text

        if "color" in kwargs:
            self.color = kwargs["color"]

    def draw(self):
        if isinstance(self.color, list):
            i = (pyxel.frame_count / 16) % len(self.color)
            pyxel.text(self.x, self.y, self.text, self.color[int(i)])
        else:
            pyxel.text(self.x, self.y, self.text, self.color)


class Button(Text):

    command = None
    borders = 7

    def __init__(self, x, y, text, **kwargs):
        Text.__init__(self, x, y, text, **kwargs)

        if "command" in kwargs:
            self.command = kwargs["command"]
        if "borders" in kwargs:
            self.borders = kwargs["borders"]

    @property
    def hovered(self):
        return super().is_colliding_xy(pyxel.mouse_x, pyxel.mouse_y)

    def update(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.hovered and self.command:
            return self.command

    def draw(self):
        super().draw()

        if self.hovered:
            pyxel.rectb(self.x - 2, self.y - 2, self.width + 3, self.height + 4, self.borders)