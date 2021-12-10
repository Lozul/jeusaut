from math import floor

import pyxel

from jeusaut.object import Object

class Lava(Object):
    def __init__(self, start, end):
        Object.__init__(self, 0, start, pyxel.width, pyxel.height)

        self.start = start
        self.end = end

    def stop(self):
        if self.y < self.start:
            self.y = min(self.y + 3, self.start)

    def update(self):
        if self.y > self.end:
            self.y -= 0.1

    def draw(self):
        pyxel.rect(self.x, floor(self.y), self.width, self.height, 8)