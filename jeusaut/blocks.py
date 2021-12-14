from time import time

import pyxel

from jeusaut.object import Object
from jeusaut.physics import Body

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

        if not self.activated and elapsed_time > 1:
            self.activated = True
            self.timer = current_time
        elif self.activated and elapsed_time > 1.5:
            self.activated = False
            self.timer = current_time

    def draw(self):
        super().draw()
        elapsed_time = time() - self.timer

        if not self.activated and elapsed_time > 0.5:
            pyxel.line(self.x, self.y, self.x + self.width - 1, self.y, 10)

        if self.activated:
            pyxel.rect(self.x, self.y - 1, self.width, 2, 13)


class Towbe(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)

        self.base_y = self.y - self.height * 3.5
        self.trap_y = self.base_y

        self.velocity = 0

        self.t = 0
        self.T = 5

    def update(self):
        if 0 <= self.t < self.T / 3:
            self.velocity += 0.9
        elif self.T / 3 <= self.t <= 2 * self.T / 3:
            self.velocity = 0
        elif 2 * self.T / 3 < self.t <= self.T:
            self.velocity -= 0.9

        self.trap_y += self.velocity

        if self.trap_y + self.height >= self.y:
            self.velocity = 0
            self.trap_y = self.y - self.height
        elif self.trap_y <= self.base_y:
            self.trap_y = self.base_y

        self.t += 1 / 30
        if self.t >= self.T:
            self.t = 0
            self.velocity = 0

    def draw(self):
        super().draw()

        pyxel.rect(self.x + 2, self.trap_y, self.width - 4, self.height, 13)
        