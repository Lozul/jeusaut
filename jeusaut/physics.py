import pyxel

from jeusaut.object import Object

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