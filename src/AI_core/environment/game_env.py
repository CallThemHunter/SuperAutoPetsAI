from typing import Optional, Union, Tuple

import gym
from gym.spaces import Discrete, Dict

from .API import EngineAPI
from ...core import Engine

_num_actions = 99
_num_packs = 2
_num_units = 120
_num_equip = 30
_max_gold = 25
_max_turn = 20


class SAPGame(gym.Env):
    def __init__(self, mode: str = "base pack"):
        self._interface = EngineAPI(Engine(mode))

        # move      25  5 5
        # combine   25  5 5
        # sell      5   5
        # buy       35  7 5
        # freeze    7
        # reroll    1
        # end turn  1
        # total     99
        self.action_space = Discrete(_num_actions)

        # 5 * 4 team
        # 7 * 5 shop
        # 6
        # 61 total
        self.observation_space = Dict({
            "team": Dict({
                "slot 1": Dict({
                    "unit": Discrete(_num_units),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "held": Discrete(_num_equip)
                }),
                "slot 2": Dict({
                    "unit": Discrete(_num_units),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "held": Discrete(_num_equip)
                }),
                "slot 3": Dict({
                    "unit": Discrete(_num_units),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "held": Discrete(_num_equip)
                }),
                "slot 4": Dict({
                    "unit": Discrete(_num_units),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "held": Discrete(_num_equip)
                }),
                "slot 5": Dict({
                    "unit": Discrete(_num_units),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "held": Discrete(_num_equip)
                }),
            }),
            "shop": Dict({
                "slot 1": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                }),
                "slot 2": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                }),
                "slot 3": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                }),
                "slot 4": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                }),
                "slot 5": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                }),
                "slot 6": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                }),
                "slot 7": Dict({
                    "item": Discrete(_num_units + _num_equip),
                    "atk": Discrete(50, start=1),
                    "hp": Discrete(50, start=1),
                    "frozen": Discrete(2),
                    "cost": Discrete(4)
                })
            }),
            "gold": Discrete(_max_gold),
            "lives": Discrete(11, start=0),
            "wins": Discrete(11, start=0),
            "turn": Discrete(_max_turn, start=1),
            "battle lost": Discrete(2),
            "pack": Discrete(_num_packs)
        })

        # hearts lost worth -0.5 per heart
        # wins worth +1.0
        # start with 10 hearts, 0 wins
        # losses worth up to -1.5, wins worth 1.0
        self.reward_range = (self._interface.loss_reward * 3, self._interface.win_reward)

        self.metadata = {"render modes": ["human", "ansi"]}

        self._cmd_cache = []
        self._create_action_cache()

    def _create_action_cache(self):
        for i in range(25):
            self._cmd_cache.append(["move", i // 5, i % 5])

        for i in range(25):
            self._cmd_cache.append(["combine", i // 5, i % 5])

        for i in range(5):
            self._cmd_cache.append(["sell", i])

        for i in range(35):
            self._cmd_cache.append(["buy", i // 5, i % 5])

        for i in range(7):
            self._cmd_cache.append(["freeze", i])

        self._cmd_cache.append(["reroll"])

        self._cmd_cache.append(["end turn"])

    def step(self, action: int) \
            -> Tuple[Dict, float, bool, dict]:
        """
        Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return
            undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, logging,
            and sometimes learning)
        """

        observation, reward, done, info = self._interface.action(*self._cmd_cache[action])
        return observation, reward, done, info

    def reset(self, *, seed: Optional[int] = None, return_info: bool = False, options: dict = None) \
            -> Union[Dict, Tuple[Dict, dict]]:
        """
        Resets the environment to an initial state and returns an initial
        observation.

        This method should also reset the environment's random number
        generator(s) if `seed` is an integer or if the environment has not
        yet initialized a random number generator. If the environment already
        has a random number generator and `reset` is called with `seed=None`,
        the RNG should not be reset.
        Moreover, `reset` should (in the typical use case) be called with an
        integer seed right after initialization and then never again.

        Returns:
            observation (object): the initial observation.
            info (optional dictionary): a dictionary containing extra information, this is only returned if
            return_info is set to true
        """
        # Initialize the RNG if the seed is manually passed

        self._interface.reset(options["mode"])
        return self._interface.current_state()

    def render(self, mode="human"):
        """
        Renders the environment.

        The set of supported modes varies per environment. (And some
        third-party environments may not support rendering at all.)
        By convention, if mode is:

        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return a numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).

        Note:
            Make sure that your class's metadata 'render_modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.

        Args:
            mode (str): the mode to render with
    """
        pass
