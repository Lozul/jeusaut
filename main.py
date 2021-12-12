""" TODO

- add "game state": for main menu, pause, game over screen etc... (will be useful to regenerate map while upgrading its generation)
- better map generation
- multiplayer: split screen for two players
- animate ground shifting
"""
import pyxel

from jeusaut.game_engine import GameEngine
from jeusaut.game_states import MainState

if __name__ == "__main__":
    pyxel.init(80, 128, fps=30, quit_key=pyxel.KEY_NONE)
    pyxel.mouse(True)

    game = GameEngine()
    game.change_state(MainState)

    pyxel.run(game.update, game.draw)