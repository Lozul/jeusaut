from time import time

import pyxel

from jeusaut.physics import Body
from jeusaut.blocks import *

class Buddy(Body):
    def __init__(self, x, y, width, height, ground):
        Body.__init__(self, x, y, width, height, ground)

        self.jump_height = 5

        self.max_hp = 3
        self.hp = self.max_hp

        self.invicible_timer = 0
        self.max_invicible_time = 2

    @property
    def can_jump(self):
        return self.grounded

    @property
    def taking_damage(self):
        b = self.ground[1]

        spiked = isinstance(b, Spike) and b.activated
        towbed = isinstance(b, Towbe) and b.trap_y + b.height >= self.y

        return spiked or towbed

    @property
    def is_invicible(self):
        return self.invicible_timer > 0

    def jump(self):
        self.y_velocity = -self.jump_height
        self.grounded = False

    def update(self):
        if self.taking_damage and not self.is_invicible:
            self.hp -= 1
            self.invicible_timer = time()

        if self.is_invicible and time() - self.invicible_timer >= self.max_invicible_time:
            self.invicible_timer = 0

        super().update()

    def draw(self):
        col = 3 if self.is_invicible else 5
        pyxel.rect(self.x, self.y, self.width, self.height, col)
        pyxel.rectb(self.x, self.y, self.width, self.height, 6)

        for i in range(self.max_hp):
            x = 2 + 8 * i

            if i < self.hp:
                pyxel.circ(x, 2, 2, 8)
            else:
                pyxel.circb(x, 2, 2, 8)