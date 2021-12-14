from random import random

from jeusaut.blocks import *

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
            new_block = Towbe(x, y)

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