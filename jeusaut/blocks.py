from time import time

import pyxel

from jeusaut.object import Object

class Block(Object):
    width = 16
    height = 16

    def __init__(self, x, y):
        Object.__init__(self, x, y, self.width, self.height)

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 4)
        pyxel.rectb(self.x, self.y, self.width, self.height, 2)


class Spike(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)

        self.timer = time()

        self.activated = False

    def update(self):
        current_time = time()
        elapsed_time = current_time - self.timer

        if not self.activated and elapsed_time > 2:
            self.activated = True
            self.timer = current_time
        elif self.activated and elapsed_time > 1:
            self.activated = False
            self.timer = current_time

    def draw(self):
        super().draw()
        elapsed_time = time() - self.timer

        if not self.activated and elapsed_time > 1:
            pyxel.line(self.x, self.y, self.x + self.width - 1, self.y, 10)

        if self.activated:
            pyxel.rect(self.x, self.y - 1, self.width, 2, 13)