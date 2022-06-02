import random
from typing import List, Optional, Dict

from . import Animal, Empty


def send_to_front(idx, team: 'Team'):
    if idx == 0:
        return

    if isinstance(team[idx], Empty):
        return

    if isinstance(team[idx - 1], Empty):
        team[idx - 1] = team[idx]
        team[idx] = Empty()
        send_to_front(idx - 1, team)
        return


def push_unit_back_one_space(team: 'Team', idx: int):
    if idx == len(team.animals) - 1:
        return

    if isinstance(team[idx + 1], Empty):
        if not isinstance(team[idx], Empty):
            team[idx + 1] = team[idx]
            team[idx] = Empty()


def push_unit_forward_one_space(team: 'Team', idx: int):
    if idx == 0:
        return

    if isinstance(team[idx - 1], Empty):
        if not isinstance(team[idx], Empty):
            team[idx - 1] = team[idx]
            team[idx] = Empty()


class Team:
    """
    handles interacting with a team, useful for getting unit lists to apply effects to
    attacking (front and right) animal is in position 0
    """

    def __init__(self):
        self.__max_capacity = 5
        self.animals: List[Animal] = [Empty() for _ in range(self.__max_capacity)]
        # self.acting = 0
        # random.seed(1)

    def __eq__(self, other: 'Team') -> bool:
        if type(other) != type(self):
            return False
        for key in other.__dict__:
            if key in self.__dict__:
                if self.__dict__[key] != other.__dict__[key]:
                    return False
            else:
                return False
        return True

    def __delitem__(self, key):
        self.animals[key] = Empty()

    def __getitem__(self, item: int) -> Animal:
        return self.animals[item]

    def __repr__(self) -> str:
        out = ""
        anims: List[Animal] = self.animals.copy()
        anims.reverse()
        for anim in anims:
            out += anim.__class__.__name__ + f" ({anim.tier})" + " "
        return out

    def __setitem__(self, idx: int, value: Animal):
        self.animals[idx] = value

    @property
    def has_lvl3(self) -> bool:
        for animal in self.animals:
            if animal.level == 3:
                return True
        return False

    @property
    def has_summon_space(self) -> bool:
        return self.size < self.__max_capacity

    @property
    def leftmost_unit(self) -> Optional[Animal]:
        if self.size == 0:
            return None

        i = len(self.animals)-1
        while isinstance(self.animals[i], Empty):
            i -= 1
        return self.animals[i]

    def level_of_actor(self, acting: int) -> int:
        # level of currently acting team member
        return self.animals[acting].level

    @property
    def rightmost_unit(self) -> Optional[Animal]:
        if self.size == 0:
            return None
        i = 0
        while isinstance(self.animals[i], Empty):
            # TODO will probably have to make it check for battle hp?
            i += 1
        return self.animals[i]

    @property
    def second_unit(self) -> Optional[Animal]:
        if self.size <= 1:
            return None
        j = 0
        i = 0
        while j != 2 and i < self.__max_capacity:
            if not isinstance(self.animals[i], Empty):
                j += 1
            i += 1
        return self.animals[i - 1]

    @property
    def size(self) -> int:
        i = 0
        for animal in self.animals:
            if not isinstance(animal, Empty):
                i += 1
        return i

    def faint(self, acting: int):
        """
        does not handle faint effects or held items that trigger on faint!
        Args:
            acting:
        Returns:
        """
        self.animals[acting] = Empty()

    def friends(self, acting: int) -> Optional[List[Animal]]:
        a = list(range(0, 5))
        a.remove(acting)
        for i in a.copy():
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if not a:
            return None
        return [self.animals[i] for i in a]

    def friend_ahead(self, acting: int) -> Optional[Animal]:
        for j in range(acting - 1, -1, -1):
            if not isinstance(self.animals[j], Empty):
                return self.animals[j]
        return None

    def friends_ahead(self, acting: int, n: int) -> Optional[List[Animal]]:
        ret = []
        i = 0
        for j in range(acting - 1, -1, -1):
            if not isinstance(self.animals[j], Empty):
                if i < n:
                    ret += [self.animals[j]]
                    i += 1
        if not ret:
            return None
        return ret

    def friend_behind(self, acting: int) -> Optional[Animal]:
        for j in range(acting + 1, len(self.animals)):
            if not isinstance(self.animals[j], Empty):
                return self.animals[j]
        return None

    def friends_behind(self, acting: int, n: int) -> Optional[List[Animal]]:
        ret = []
        i = 0
        for j in range(acting + 1, len(self.animals)):
            if not isinstance(self.animals[j], Empty):
                if i < n:
                    ret += [self.animals[j]]
                    i += 1
        if not ret:
            return None
        return ret

    def highest_health_unit(self):
        return max(self.animals, key=lambda animal: animal.battle_hp)

    def lowest_health_unit(self):
        return min(self.animals, key=lambda animal: animal.battle_hp)

    def make_summon_room_with_left_shift_at(self, idx: int):
        last_empty = 4
        for i in range(self.__max_capacity - 1, idx - 1, -1):
            if isinstance(self.animals[i], Empty):
                last_empty = i

        for i in range(last_empty - 1, idx - 1, -1):
            push_unit_back_one_space(self, i)

    def make_summon_room_with_right_shift_at(self, idx: int):
        last_empty = 0
        for i in range(0, idx + 1):
            if isinstance(self.animals[i], Empty):
                last_empty = i

        for i in range(last_empty + 1, idx + 1):
            push_unit_forward_one_space(self, i)

    def mark_fainted(self, pos: int):
        self.animals[pos].battle_hp = 0

    def other_lvl2_or_3(self, acting: int) -> Optional[List[Animal]]:
        a = list(range(0, 5))
        a.remove(acting)
        for i in a.copy():
            if self.animals[i].level <= 1:
                a.remove(i)
        if not a:
            return None
        return [self.animals[i] for i in a]

    def push_forward(self):
        for i, _ in enumerate(self.animals):
            send_to_front(i, self)
        return

    def random_friend(self, acting: int) -> Optional[Animal]:
        a = list(range(0, 5))
        a.remove(acting)
        for i in a.copy():
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if not a:
            return None
        return self.animals[random.choice(a)]

    def random_friends(self, acting: int, n: int) -> Optional[List[Animal]]:
        a = list(range(0, 5))
        a.remove(acting)
        for i in a.copy():
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if not a:
            return None
        if len(a) < n:
            return [self.animals[i] for i in a]
        else:
            return random.sample([self.animals[i] for i in a], n)

    def random_unit(self) -> Optional[Animal]:
        if self.size == 0:
            return None

        a = list(range(0, 5))
        for i in a.copy():
            if isinstance(self.animals[i], Empty):
                a.remove(i)

        return self.animals[random.choice(a)]

    def random_units(self, n) -> Optional[List[Animal]]:
        if self.size == 0:
            return None

        a = list(range(0, 5))
        for i in a.copy():
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if not a:
            return None
        if len(a) <= n:
            return [self.animals[i] for i in a]
        else:
            return random.sample([self.animals[i] for i in a], n)

    def random_units_idx(self, n) -> Optional[List[int]]:
        a = list(range(0, 5))
        for i in a.copy():
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if not a:
            return None
        if len(a) <= n:
            return a
        else:
            return random.sample(a, n)

    def ret_diff_tiers(self) -> Optional[List[Animal]]:
        animals: Dict = {}
        for animal in self.animals:
            if not isinstance(animal, Empty):
                animals[animal.tier] = animal

        animals: List[Animal] = list(animals.values())
        if not animals:
            return None
        return animals

    def summon(self, animal, position) -> bool:
        """
        assume all units are pushed forward when called
        Args:
            animal:
            position:

        Returns:

        """
        if self.size == 5:
            return False

        self.make_summon_room_with_left_shift_at(position)
        if isinstance(self[position], Empty):
            self[position] = animal
            return True
        return False

    def units(self) -> Optional[List[Animal]]:
        out = []
        for animal in self.animals:
            if not isinstance(animal, Empty):
                out.append(animal)

        if not out:
            return None

        return out
