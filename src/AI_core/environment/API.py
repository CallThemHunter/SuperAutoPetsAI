from typing import Optional

from src.core import Engine

__all__ = ['EngineAPI']

_limit = 50


class EngineAPI:
    loss_reward = -0.5
    win_reward = 1.0
    invalid_move_penalty = -0.01

    def __init__(self, engine: Engine):

        self.engine = engine

        self._action_lookup = {
            "sell": self._sell,
            "buy": self._buy,
            "reroll": self._reroll,
            "end turn": self._end_turn,
            "freeze": self._freeze,
            "move": self._move,
            "combine": self._combine
        }

        self.__actions_this_turn = 0

    def action(self, *args):
        """
        Processes action state commands into engine readable commands
        Args:
            *args: arg[0] is action id
                   arg[1:] is information needed for that action

        Returns:

        """

        wins = self.engine.messenger.wins
        lives = self.engine.messenger.life

        if self.__actions_this_turn == _limit:
            penalty = self._action_lookup["end turn"]()
        else:
            penalty = self._action_lookup[args[0]](*args[1:])

        life_change = lives - self.engine.messenger.life

        reward = self.win_reward * (self.engine.messenger.wins - wins) + self.loss_reward * life_change
        reward += penalty * self.invalid_move_penalty

        done = self.engine.messenger.wins == 10 or self.engine.messenger.life == 0

        return self.current_state(), reward, done, None

    def current_state(self):
        return self.engine.save(include_shop=True).as_array().reshape((1, 76))

    def reset(self, mode: Optional[str] = None):
        self.engine = self.engine.__class__(mode)
        self.__actions_this_turn = 0
        return self.current_state()

    def _sell(self, *args):
        penalty = self.engine.sell(*args[1:])
        self.__actions_this_turn -= penalty
        return penalty

    def _buy(self, *args):
        penalty = self.engine.buy(*args[1:])
        self.__actions_this_turn -= penalty
        return penalty

    def _reroll(self):
        penalty = self.engine.reroll()
        self.__actions_this_turn -= penalty
        return penalty

    def _end_turn(self):
        self.engine.end_turn()
        self.__actions_this_turn = 0
        return 0

    def _freeze(self, *args):
        penalty = self.engine.freeze(*args[1:])
        self.__actions_this_turn -= penalty - 1
        return penalty

    def _move(self, *args):
        penalty = self.engine.move(*args[1:])
        self.__actions_this_turn -= penalty - 1
        return penalty

    def _combine(self, *args):
        penalty = self.engine.combine(*args[1:])
        self.__actions_this_turn -= penalty - 1
        return penalty
