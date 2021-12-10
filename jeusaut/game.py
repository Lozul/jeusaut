import pyxel

from jeusaut.ground import Ground
from jeusaut.buddy import Buddy
from jeusaut.lava import Lava

class Game:
    def __init__(self):
        pyxel.init(80, 128)

        self.ground = Ground(6, pyxel.height / 2)

        self.buddy = Buddy(8, 0, 16, 16, self.ground.blocks)

        self.lava = Lava(start=pyxel.height, end=0)

        self.jump_released = True
        self.debug = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.buddy.hp <= 0 or self.buddy.is_colliding(self.lava):
            print("Game Over!")
            pyxel.quit()

        if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
            self.jump_released = True

        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_LEFT_BUTTON)) and self.jump_released and self.buddy.can_jump:
            self.jump_released = False

            self.buddy.jump()

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