
from jeusaut.game_states import MainState, PauseState

class GameEngine:

    _states = []
    _main_state = None
    _current_state = None

    def __init__(self):
        self._main_state = MainState()
        self._states = [PauseState()]

    def change_state(self, state_type):
        if isinstance(self._main_state, state_type):
            self._current_state = self._main_state
            return

        for i in range(len(self._states)):
            if isinstance(self._states[i], state_type):
                self._current_state = self._states[i]
                break

    def restart(self):
        self._main_state.restart()
        self.change_state(MainState)

    def update(self):
        self._current_state.update(self)

    def draw(self):
        self._current_state.draw()