""" TODO

- add "game state": for main menu, pause, game over screen etc... (will be useful to regenerate map while upgrading its generation)
- better map generation
- animate ground shifting
"""

import pyxel
import numpy as np

from time import time
from math import sin, pi, floor
from random import random


class Object:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_colliding(self, other):
        if not isinstance(other, Object):
            return False

        return not (self.x + self.width <= other.x or other.x + other.width <= self.x or self.y + self.height <= other.y or other.y + other.height <= self.y)

    def update(self):
        pass

    def draw(self):
        pass


class Body(Object):
    def __init__(self, x, y, width, height, ground):
        Object.__init__(self, x, y, width, height)

        self.y_velocity = 0
        self.grounded = False

        self.ground = ground
        self.ground_y = pyxel.height - self.height

        self.gravity = 0.8

    def is_grounded(self):
        for block in self.ground:
            if (self.y + self.height == block.y and self.x == block.x) or self.is_colliding(block):
                self.grounded = True
                self.ground_y = block.y - self.height
                break

    def update(self):
        self.y_velocity += self.gravity
        self.y += self.y_velocity

        self.is_grounded()

        if self.grounded:
            self.y_velocity = 0
            self.y = self.ground_y


class Buddy(Body):
    def __init__(self, x, y, width, height, ground):
        Body.__init__(self, x, y, width, height, ground)

        self.jump_height = 5
        self.jump_released = True

        self.max_hp = 3
        self.hp = self.max_hp

        self.invicible_timer = 0
        self.max_invicible_time = 3

    @property
    def can_jump(self):
        return self.grounded and self.jump_released

    @property
    def taking_damage(self):
        b = self.ground[1]

        return isinstance(b, Spike) and b.activated

    @property
    def is_invicible(self):
        return self.invicible_timer > 0

    def update(self):
        if self.taking_damage and not self.is_invicible:
            self.hp -= 1
            self.invicible_timer = time()

        if self.is_invicible and time() - self.invicible_timer >= self.max_invicible_time:
            self.invicible_timer = 0

        if pyxel.btn(pyxel.KEY_SPACE) and self.can_jump:
            self.y_velocity = -self.jump_height
            self.grounded = False
            self.jump_released = False

        if pyxel.btnr(pyxel.KEY_SPACE):
            self.jump_released = True

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


class Ground:
    def __init__(self, nb_blocks, base_y):
        self.blocks = []

        self.nb_blocks = nb_blocks
        self.base_y = base_y

        self.generate_ground()

    def add_new_block(self):
        i = len(self.blocks)
        x = i * Block.width - Block.width / 2
        y = self.base_y + random() * 5

        if random() > 0.2:
            new_block = Block(x, y)
        else:
            new_block = Spike(x, y)

        self.blocks.append(new_block)

    def generate_ground(self):
        self.blocks = []

        for i in range(self.nb_blocks):
            self.add_new_block()

    def shift_ground(self):
        self.blocks.pop(0)

        for block in self.blocks:
            block.x -= block.width

        self.add_new_block()

    def update(self):
        for block in self.blocks:
            block.update()

    def draw(self):
        for block in self.blocks:
            block.draw()


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


class Game:
    def __init__(self):
        pyxel.init(80, 128)

        self.ground = Ground(6, pyxel.height / 2)

        self.buddy = Buddy(8, 0, 16, 16, self.ground.blocks)
        self.current_block = 1

        self.lava = Lava(start=pyxel.height, end=0)

        self.debug = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.buddy.hp <= 0 or self.buddy.is_colliding(self.lava):
            print("Game Over!")
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_SPACE) and self.buddy.can_jump:
            self.ground.shift_ground()
            self.lava.stop()

        self.buddy.update()
        self.ground.update()
        self.lava.update()

        if pyxel.btnr(pyxel.KEY_F1):
            self.debug = not self.debug

    def draw(self):
        pyxel.cls(0)
        
        self.buddy.draw()
        self.ground.draw()
        self.lava.draw()     


def main():
    Game()

if __name__ == "__main__":
    main()