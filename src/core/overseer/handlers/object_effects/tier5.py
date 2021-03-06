from typing import TYPE_CHECKING, Tuple

from ....game_elements.abstract_elements import Animal
from ....game_elements.game_objects.equipment import Milk, Better_Milk, Best_Milk, Peanut

if TYPE_CHECKING:
    from ... import MessageAgent


class Tier5:
    @staticmethod
    def chicken(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            agent.shop.perm_buff(1, 1)
        elif agent.actor(actor).level == 2:
            agent.shop.perm_buff(2, 2)
        else:
            agent.shop.perm_buff(3, 3)

    # add cow's milk to shop
    @staticmethod
    def cow(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        # replace both slots with milk
        for slot in agent.shop.roster[5:]:
            if agent.actor(actor).level == 1:
                slot.item = Milk()
            elif agent.actor(actor).level == 2:
                slot.item = Better_Milk()
            elif agent.actor(actor).level == 3:
                slot.item = Best_Milk()

    # deal 7/14/21 damage to last enemy
    @staticmethod
    def crocodile(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int], backup: Animal):
        for _ in range(backup.level):
            target = agent.team_opposing_(actor).leftmost_unit
            if actor[0] == "team":
                target_tup = ("enemy", agent.team_opposing_(actor).animals.index(target))
            else:
                target_tup = ("team", agent.team_opposing_(actor).animals.index(target))

            agent.deal_ability_damage_handle_hurt(8, actor, target_tup, backup)

    @staticmethod
    def eagle(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int], fainted: Animal):
        unit: Animal = agent.shop[0].spawner.spawn_tier(6)

        # set stats with multiplier
        unit.atk *= fainted.level
        unit.battle_atk *= fainted.level
        unit.hp *= fainted.level
        unit.battle_hp *= fainted.level

        if fainted.level == 1:
            unit.xp = 0
        elif fainted.level == 2:
            unit.xp = 2
        else:
            unit.xp = 5

        agent.summon(unit, actor)

    # limited activation count stored in Goat object
    @staticmethod
    def goat(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        agent.gold += 1

    @staticmethod
    def monkey(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        animal_to_buff = agent.team.rightmost_unit
        if agent.actor(actor).level == 1:
            agent.buff(animal_to_buff, 2, 3)
        elif agent.actor(actor).level == 2:
            agent.buff(animal_to_buff, 4, 6)
        else:
            agent.buff(animal_to_buff, 6, 9)

    @staticmethod
    def poodle(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        animals_to_buff = agent.team.ret_diff_tiers()
        buff_amount = agent.actor(actor).level

        for animal in animals_to_buff:
            animal.permanent_buff(buff_amount, buff_amount)

    @staticmethod
    def rhino(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        target = agent.team_opposing_(actor).rightmost_unit
        if actor[0] == "team":
            target_tup = ("enemy", agent.team_opposing_(actor).animals.index(target))
        else:
            target_tup = ("team", agent.team_opposing_(actor).animals.index(target))

        agent.deal_ability_damage_handle_hurt(4 * agent.actor(actor).level,
                                              actor, target_tup)

    @staticmethod
    def scorpion(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        agent.actor(actor).held = Peanut()

    @staticmethod
    def seal(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        friends = agent.team.random_friends(actor[1], 2)
        if agent.actor(actor).level == 1:
            agent.buff(friends, 1, 1)
        elif agent.actor(actor).level == 2:
            agent.buff(friends, 2, 2)
        else:
            agent.buff(friends, 3, 3)

    @staticmethod
    def shark(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int], fainted: Animal):
        if agent.actor(actor).level == 1:
            agent.buff(agent.actor(actor), 2, 2)
        elif agent.actor(actor).level == 2:
            agent.buff(agent.actor(actor), 4, 4)
        else:
            agent.buff(agent.actor(actor), 6, 6)

    @staticmethod
    def turkey(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            agent.buff(agent.actor(target), 2, 3)
        elif agent.actor(actor).level == 2:
            agent.buff(agent.actor(target), 4, 6)
        else:
            agent.buff(agent.actor(target), 6, 9)
