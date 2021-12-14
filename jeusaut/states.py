import pyxel

from jeusaut.ground import Ground
from jeusaut.buddy import Buddy
from jeusaut.lava import Lava
from jeusaut.ui import *


class State:
    def __init__(self):
        pass

    def update(self, engine):
        pass

    def draw(self):
        pass


class MainState(State):
    def __init__(self):
        State.__init__(self)

        self.restart()

    def restart(self):
        self.ground = Ground(6, pyxel.height / 2)

        self.buddy = Buddy(8, 0, 16, 16, self.ground.blocks)

        self.lava = Lava(start=pyxel.height, end=0)

        self.jump_released = True

    def update(self, engine):
        if self.buddy.hp <= 0 or self.buddy.is_colliding(self.lava):
            print("Game Over!")
            pyxel.quit()

        if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.jump_released = True

        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)) and self.jump_released and self.buddy.can_jump:
            self.jump_released = False

            self.buddy.jump()

            self.ground.shift_ground()
            self.lava.stop()

        if pyxel.btnr(pyxel.KEY_P) or pyxel.btnr(pyxel.KEY_ESCAPE):
            engine.change_state(PauseState)

        self.buddy.update()
        self.ground.update()
        self.lava.update()

    def draw(self):
        pyxel.cls(0)
        
        self.ground.draw()
        self.buddy.draw()
        self.lava.draw()


class PauseState(State):
    def __init__(self):
        State.__init__(self)
        y = pyxel.height / 2 - 18

        self.ui = [
            Text(pyxel.width / 2 - 10, y, "Pause", color=6),
            Button(pyxel.width / 2 - 14, y + 15, "Restart", command="restart", color=14),
            Button(pyxel.width / 2 - 8, y + 30, "Quit", command="quit", color=14)
        ]

    def update(self, engine):
        if pyxel.btnr(pyxel.KEY_P) or pyxel.btnr(pyxel.KEY_ESCAPE):
            engine.change_state(MainState)

        if pyxel.btn(pyxel.KEY_R):
            engine.restart()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        for item in self.ui:
            res = item.update()

            if res == "quit":
                pyxel.quit()
            elif res == "restart":
                engine.restart()

    def draw(self):
        pyxel.cls(1)

        for item in self.ui:
            item.draw()