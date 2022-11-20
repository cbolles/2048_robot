import tensorflow as tf
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.specs import array_spec
from twenty.model import GameModel
import copy


class GameEnvironment(PyEnvironment):
    """
    Implementation of the tensorflow agent environment for the 2048 game
    """
    def __init__(self, game: GameModel):
        # Keep track of the initial game for resetting
        self.initial_board = copy.deepcopy(game)

        self.game = game
        # The action correspond to the direction of the move
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')
        # The observation is the board state
        self._observation_spec = array_spec.BoundedArraySpec(shape=(4, 4), dtype=np.int32, minimum=0, maximum=2048, name='observation')
        # The reward is the score
        self._reward_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, name='reward')

        # Keep track of the current state of the board
        self._state = self.game.board
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def reward_spec(self):
        return self._reward_spec

    def _reset(self):
        self.game = copy.deepcopy(self.initial_board)
        self._state = self.game.board
        self._episode_ended = False
        return ts.restart(self._state)

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        # Perform the action
        self.game.move(action)

        # Check if the game is over
        if self.game.is_over():
            self._episode_ended = True
            return ts.termination(self._state, self.game.score)

        return ts.transition(self._state, reward=self.game.score, discount=1.0)
