""" TODO

- better map generation
- multiplayer: split screen for two players
- animate ground shifting
"""
import pyxel

from jeusaut.engine import Engine
from jeusaut.states import MainState

if __name__ == "__main__":
    pyxel.init(80, 128, fps=30, quit_key=pyxel.KEY_NONE)
    pyxel.mouse(True)

    game = Engine()
    game.change_state(MainState)

    pyxel.run(game.update, game.draw)