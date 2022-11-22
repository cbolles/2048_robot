import tensorflow as tf
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.specs import array_spec
from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks.q_network import QNetwork
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.policies import random_tf_policy
from tf_agents.metrics import tf_metrics
from tf_agents.drivers import dynamic_step_driver, dynamic_episode_driver
from tf_agents.policies import py_tf_policy
from tf_agents.policies.policy_saver import PolicySaver
import tf_agents.trajectories.time_step as ts
from tf_agents.environments import tf_py_environment
from twenty.model import GameModel, Direction
import copy
import numpy as np


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
        self._state = self.game.tiles
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def reward_spec(self):
        return self._reward_spec

    def _reset(self):
        self.game = copy.deepcopy(self.initial_board)
        self._state = self.game.tiles
        self._episode_ended = False
        return ts.restart(self._state)

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        # Perform the action
        self.game = self.game.move(Direction(action))
        self._state = self.game.tiles

        # Check if the game is over
        if self.game.game_over():
            self._episode_ended = True
            return ts.termination(self._state, self.game.score)

        return ts.transition(self._state, reward=self.game.score, discount=1)


def train():
    # Hyperparameters
    num_iterations = 20000
    initial_collect_steps = 100
    collect_steps_per_iteration = 1
    replay_buffer_max_length = 100000

    batch_size = 64
    learning_rate = 1e-3
    log_interval = 200

    num_eval_episodes = 10
    eval_interval = 1000

    initial_tiles = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 2]
    ]
    # Create the game
    game = GameModel(initial_tiles)

    env = GameEnvironment(game)
    env = tf_py_environment.TFPyEnvironment(env)
    env.reset()

    print('Observation Spec:')
    print(env.observation_spec())
    print('Action Spec:')
    print(env.action_spec())
    print('Reward Spec:')
    print(env.reward_spec())

    time_step = env.reset()
    print('Time step:')
    print(time_step)

    action = np.array(1, dtype=np.int32)
    next_time_step = env.step(action)
    print('Next time step:')
    print(next_time_step)
