
from jeusaut.game_states import MainState, PauseState

class GameEngine:

    _states = []
    _current_state = None

    def __init__(self):
        self._states = [MainState(), PauseState()]

    def change_state(self, state_type):
        for i in range(len(self._states)):
            if isinstance(self._states[i], state_type):
                self._current_state = self._states[i]
                break

    def update(self):
        self._current_state.update(self)

    def draw(self):
        self._current_state.draw()