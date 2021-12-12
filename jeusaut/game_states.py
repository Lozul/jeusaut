import pyxel

from jeusaut.ground import Ground
from jeusaut.buddy import Buddy
from jeusaut.lava import Lava
from jeusaut.ui import *


class GameState:
    def __init__(self):
        pass

    def update(self, game_engine):
        pass

    def draw(self):
        pass


class MainState(GameState):
    def __init__(self):
        GameState.__init__(self)

        self.ground = Ground(6, pyxel.height / 2)

        self.buddy = Buddy(8, 0, 16, 16, self.ground.blocks)

        self.lava = Lava(start=pyxel.height, end=0)

        self.jump_released = True

    def update(self, game_engine):
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
            game_engine.change_state(PauseState)

        self.buddy.update()
        self.ground.update()
        self.lava.update()

    def draw(self):
        pyxel.cls(0)
        
        self.buddy.draw()
        self.ground.draw()
        self.lava.draw()


class PauseState(GameState):
    def __init__(self):
        self.ui = [Button(pyxel.width / 2 - 8, pyxel.height - 20, "Quit", pyxel.quit)]

    def update(self, game_engine):
        if pyxel.btnr(pyxel.KEY_P) or pyxel.btnr(pyxel.KEY_ESCAPE):
            game_engine.change_state(MainState)

        for item in self.ui:
            item.update()

    def draw(self):
        pyxel.cls(0)

        x, y = pyxel.width / 2 - 10, 20

        pyxel.text(x + 1, y + 1, "PAUSE", 5)
        pyxel.text(x, y, "PAUSE", 6)

        for item in self.ui:
            item.draw()