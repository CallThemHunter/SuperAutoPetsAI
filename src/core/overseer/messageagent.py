import itertools
from typing import List, Callable, Tuple, Union

from ..game_elements.abstract_elements import Animal, Empty
from .state import State
from .baseagent import BaseAgent
from .handlers.object_effects import Tier1, Tier2, Tier3, Tier4, Tier5, Tier6, Equipment
from .handlers.eventprocessor import EventProcessor
from .. import eventnames

animals = [
    "Nop",  # No action

    "Ant", "Beaver", "Beetle", "Bluebird", "Cricket", "Duck", "Fish", "Horse", "Ladybug", "Mosquito", "Otter",
    "Pig",  # Tier 1

    "Bat", "Crab", "Dodo", "Dromedary", "Elephant", "Flamingo", "Hedgehog", "Peacock", "Rat", "Shrimp",
    "Spider", "Swan", "Tabby Cat",  # Tier 2

    "Badger", "Blowfish", "Camel", "Caterpillar", "Dog", "Giraffe", "Hatching Chick", "Kangaroo", "Owl", "Ox", "Puppy",
    "Rabbit", "Sheep", "Snail", "Tropical Fish", "Turtle",  # Tier 3

    "Bison", "Buffalo", "Deer", "Dolphin", "Hippo", "Llama", "Lobster", "Microbe", "Parrot", "Penguin",
    "Rooster", "Skunk", "Squirrel", "Whale", "Worm",  # Tier 4

    "Chicken", "Cow", "Crocodile", "Eagle", "Goat", "Monkey", "Poodle", "Rhino", "Scorpion", "Seal", "Shark",
    "Turkey",  # Tier 5

    "Boar", "Cat", "Dragon", "Fly", "Gorilla", "Leopard", "Mammoth", "Octopus", "Sauropod", "Snake", "Tiger",
    "Tyrannosaurus"  # Tier 6

    "Butterfly", "Bus", "Dirty_Rat", "Fly_Friend", "Ram", "Zombie_Cricket"
]

equipment = [
    "Apple", "Honey",  # Tier 1
    "Cupcake", "Meat Bone", "Sleeping Pill", "Weak"  # Tier 2
                                             "Garlic", "Salad Bowl",  # Tier 3
    "Canned Food", "Pear",  # Tier 4
    "Best Milk", "Better Milk", "Chili", "Chocolate", "Milk", "Peanut", "Sushi",  # Tier 5
    "Coconut", "Melon", "Mushroom", "Pizza", "Steak"  # Tier 6
]


def find_name_id(anims: List[List[Animal]], name: str) -> int:
    for tier in anims:
        for anim in tier:
            anim_name: str = anim.__class__.__name__.lower()
            if anim_name == name:
                return anim.id
    return -1


class MessageAgent(BaseAgent):
    def __init__(self, mode):
        super(MessageAgent, self).__init__(mode)
        # event handling matrix
        t1 = Tier1()
        t2 = Tier2()
        t3 = Tier3()
        t4 = Tier4()
        t5 = Tier5()
        t6 = Tier6()
        eq = Equipment()
        # objs = [t1, t2, t3, t4, t5, t6, Equipment]
        self.__EP = EventProcessor()

        # THIS IS DICTATED BY UNIT IDS. DO NOT MESS WITH ORDER
        self.func: List[Union[
            Callable[['MessageAgent', Tuple[str, int], Tuple[str, int]], None],
            Callable[['MessageAgent', Tuple[str, int], Tuple[str, int], Animal], None]]
        ] = [
            t1.nop,

            t1.ant, t1.beaver, t1.beetle, t1.bluebird, t1.cricket,
            t1.duck, t1.fish, t1.horse, t1.ladybug, t1.mosquito,
            t1.otter, t1.pig,

            t2.bat, t2.crab, t2.dodo, t2.dromedary, t2.elephant,
            t2.flamingo, t2.hedgehog, t2.peacock, t2.rat, t2.shrimp,
            t2.spider, t2.swan, t2.tabby_cat,

            t3.badger, t3.blowfish, t3.camel, t3.caterpillar, t3.dog,
            t3.giraffe, t3.hatching_chick, t3.kangaroo, t3.owl, t3.ox,
            t3.puppy, t3.rabbit, t3.sheep, t3.snail, t3.tropical_fish,
            t3.turtle,

            t4.bison, t4.buffalo, t4.deer, t4.dolphin, t4.hippo,
            t4.llama, t4.lobster, t4.penguin, t4.poodle, t4.rooster,
            t4.skunk, t4.squirrel, t4.whale, t4.worm,

            t5.chicken, t5.cow, t5.crocodile, t5.eagle, t5.goat,
            t5.microbe, t5.monkey, t5.parrot, t5.rhino, t5.scorpion,
            t5.seal, t5.shark, t5.turkey,

            t6.boar, t6.cat, t6.dragon, t6.fly, t6.gorilla, t6.leopard,
            t6.mammoth, t6.octopus, t6.sauropod, t6.snake, t6.tiger,
            t6.tyrannosaurus
        ]

        # room for new units, just have ids be after t-rex

        num_nops = 400 - len(self.func)
        self.func += [t1.nop for _ in range(num_nops)]

        self.func += [
            eq.apple, eq.honey,
            eq.cupcake, eq.meat_bone, eq.sleeping_pill, eq.weak,
            eq.garlic, eq.salad_bowl,
            eq.canned_food, eq.pear,
            eq.best_milk, eq.better_milk, eq.chili, eq.chocolate, eq.milk, eq.peanut, eq.sushi,
            eq.coconut, eq.melon, eq.mushroom, eq.pizza, eq.steak
        ]

        self._event_queue = []
        self._root_event = True
        # self.functions = {}
        #
        # for group in objs:
        #     members = inspect.getmembers(group)
        #     for member in members:
        #         if isinstance(member[1], FunctionType):
        #             # have to get member id!!
        #             anim_id = find_name_id(_animals, member[0])
        #             if anim_id != -1:
        #                 self.functions[anim_id] = member[1]

    def sorted_team(self, team: str = None):
        # for unit in roster sorted by descending attack, then decreasing index
        if team == "team" or team is None:
            roster = self.team.animals
        elif team == "enemy":
            roster = self.enemy.animals
        elif team == "both":
            # interleaved units to maintain left/right ordering for enemies and friendlies
            roster = list(itertools.chain(*zip(self.team.animals, self.enemy.animals)))
        else:
            raise ValueError(f"self.event_raiser should not contain {self.event_raiser[0]}")

        units_sorted = sorted(
            roster,
            key=lambda animal: (animal.atk, roster.index(animal)),
            reverse=True)

        # remove all empty spaces!
        while Empty() in units_sorted:
            units_sorted.remove(Empty())

        return units_sorted

    def sorted_without_(self, actor: Tuple[str, int]):
        sorted_team = self.sorted_team(actor[0])
        if actor[0] == "team":
            sorted_team.remove(self.team.animals[actor[1]])
            return sorted_team
        elif actor[0] == "enemy":
            sorted_team.remove(self.enemy.animals[actor[1]])
            return sorted_team
        raise ValueError(f"self.event_raiser should not contain {actor[0]}")

    def sorted_units_behind_(self, actor: Tuple[str, int]):
        sorted_team = self.sorted_team(actor[0])
        if actor[0] == "team":
            out = []
            for animal in sorted_team:
                if self.team.animals.index(animal) > actor[1]:
                    out += [animal]
            return out
        elif actor[0] == "enemy":
            out = []
            for animal in sorted_team:
                if self.enemy.animals.index(animal) > actor[1]:
                    out += [animal]
            return out
        raise ValueError(f"self.event_raiser should not contain {actor[0]}")

    @staticmethod
    def load(state: State) -> 'BaseAgent':
        agent = MessageAgent(state.mode)
        agent.turn = state.turn
        agent.life = state.life
        agent.gold = state.gold
        agent.battle_lost = state.battle_lost
        agent.team = state.team
        agent.shop = state.shop
        return agent

    def _raise_event(self):
        tup = self._event_queue.pop(0)
        if len(tup) == 4:
            (message, actor, target, fainted) = tup
        else:
            (message, actor, target) = tup
            fainted = None

        # sending messages like buy, sell, move, combine, start turn, end turn,

        # route to trigger processor, it will figure out which units to have
        # handle messages.
        # start turn, reroll, freeze/unfreeze, hurt, faint, knock out, attacks,
        # before attack, unit ahead attacks, unit ahead faints, friend summoned

        # raise event
        if message == eventnames.ATTACK:
            self.attack(actor, target)

        elif message == eventnames.BEFORE_ATTACK:
            self.__EP.before_attack(self, actor)
        elif message == eventnames.BUY:
            self.__EP.buy(self, actor)
        elif message == eventnames.BUY_FOOD:
            self.__EP.buy_food(self)
        elif message == eventnames.BUY_T1_PET:
            self.__EP.buy_t1_pet(self)
        elif message == eventnames.EAT_FOOD:
            self.__EP.eat_food(self, actor)
        elif message == eventnames.ENEMY_ATTACKS:
            self.__EP.enemy_attacks(self, actor)
        elif message == eventnames.END_TURN:
            self.__EP.end_turn(self)
        elif message == eventnames.FRIEND_AHEAD_ATTACKS:
            self.__EP.friend_ahead_attacks(self, actor)
        elif message == eventnames.FRIEND_AHEAD_FAINTS:
            # special faint function
            self.__EP.friend_ahead_faints(self, actor, fainted)
        elif message == eventnames.FRIEND_BOUGHT:
            self.__EP.friend_bought(self, actor)
        elif message == eventnames.FRIEND_EATS_FOOD:
            self.__EP.friend_eats_food(self, actor)
        elif message == eventnames.FRIEND_FAINTS:
            # special faint function
            self.__EP.friend_faints(self, actor, fainted)
        elif message == eventnames.FRIEND_SOLD:
            self.__EP.friend_sold(self, actor)
        elif message == eventnames.FRIEND_SUMMONED_BATTLE:
            self.__EP.friend_summoned_battle(self, actor)
        elif message == eventnames.FRIEND_SUMMONED_SHOP:
            self.__EP.friend_summoned_shop(self, actor)
        elif message == eventnames.HURT:
            self.__EP.hurt(self, actor)
        elif message == eventnames.IS_SUMMONED:
            self.__EP.is_summoned(self, actor)
        elif message == eventnames.KNOCK_OUT:
            self.__EP.knock_out(self, actor)
        elif message == eventnames.ON_FAINT:
            # special faint function
            self.__EP.on_faint(self, actor, fainted)
        elif message == eventnames.ON_LEVEL:
            self.__EP.on_level(self, actor)
        elif message == eventnames.SELL:
            self.__EP.sell(self, actor)
        elif message == eventnames.START_BATTLE:
            self.__EP.start_battle(self)
        elif message == eventnames.START_TURN:
            self.__EP.start_turn(self)

    def enqueue_event(self, message, actor: Tuple[str, int] = None, target: Tuple[str, int] = None,
                      fainted: Animal = None):
        if fainted is None:
            self._event_queue.append((message, actor, target, fainted))
        else:
            self._event_queue.append((message, actor, target))

    def handle_events(self):
        if not self._event_queue:
            return

        self._raise_event()
        self.handle_events()
        return

    # message contains unit_id which sent it
    def trigger_ability(self, message: int, actor: Tuple[str, int], target: Tuple[str, int], fainted: Animal = None):
        # trigger function that manipulates roster
        # does not return anything
        if fainted is None:
            self.func[message](self, actor, target)
        else:
            self.func[message](self, actor, target, fainted)

    # assume event which triggered event handler has already resolved!!!
    # e.g. if animal sold, then it is no longer in the roster and gold
    # incremented already
    # also assume that self.lvl is the level of the unit whose ability triggered
    # done for convenience, otherwise it's a pain...

    def _query_faint(self, actor: Tuple[str, int], target: Tuple[str, int]) -> bool:
        """
        check if actor faints. may trigger knockout event
        Args:
            actor:
            target:
        Returns: TRUE
        """
        if self.actor(actor).battle_hp < 1:
            self.faint(actor, target)
            return False
        else:
            return True

    def attack(self, actor: Tuple[str, int], target: Tuple[str, int]):
        """
        handles one attack flow.
        Args:
            actor:
            target:
        Returns:

        """
        actor_damage_taken, target_damage_taken = self.deal_attack_damage(actor, target)

        if actor_damage_taken != 0:
            if self._query_faint(actor, target):
                self.enqueue_event(eventnames.HURT,
                                   actor=self.event_raiser,
                                   target=self.target)

        if target_damage_taken != 0:
            if self._query_faint(target, actor):
                self.enqueue_event(eventnames.HURT,
                                   actor=self.target,
                                   target=self.event_raiser)

    def deal_ability_damage_handle_hurt(self, damage: int, actor: Union[Tuple[str, int], Animal],
                                        target: Tuple[str, int]):
        """
        actor deals damage
        target receives damage
        Args:
            damage:
            actor:
            target:
        Returns:
        """

        if isinstance(actor, Animal):
            damage = actor.damage_modifier(self, damage, "ability")
        else:
            damage = self.actor(actor).damage_modifier(self, damage, "ability")

        damage = self.actor(target).damage_modifier(self, damage, "incoming")

        if damage == 0:
            return

        self.actor(target).battle_hp -= damage
        if not self._query_faint(target, actor):
            self.enqueue_event(eventnames.HURT,
                               actor=target,
                               target=actor)

    def deal_attack_damage(self, actor: Tuple[str, int], target: Tuple[str, int]) -> Tuple[int, int]:
        """
        accounts for held items of attacker (event raiser) and attackee (target)
        you must set attacker and attackee beforehand
        does not call any events
        Args:
            actor:
            target:
        """
        target_anim = self.actor(target)
        actor_anim = self.actor(actor)

        actor_damage_taken = target_anim.damage_modifier(self, target_anim.battle_atk, "outgoing")
        actor_damage_taken = actor_anim.damage_modifier(self, actor_damage_taken, "incoming")

        target_damage_taken = actor_anim.damage_modifier(self, actor_anim.battle_atk, "outgoing")
        target_damage_taken = target_anim.damage_modifier(self, target_damage_taken, "incoming")

        target_anim.battle_hp -= target_damage_taken
        actor_anim.battle_hp -= actor_damage_taken
        return actor_damage_taken, target_damage_taken

    def deal_sneak_damage_handle_hurt(self, actor: Tuple[str, int], target: Tuple[str, int], damage):
        target_anim = self.actor(target)
        damage = target_anim.damage_modifier(self, damage, "incoming")

        if damage == 0:
            return

        target_anim.battle_hp -= damage
        if not self._query_faint(actor, target):
            self.enqueue_event(eventnames.HURT,
                               actor=target,
                               target=actor)

    def faint(self, actor: Tuple[str, int], target: Tuple[str, int]):
        # faint the actor!
        # target dealt the killing blow!

        animal = self.actor(actor)

        self.enqueue_event(eventnames.ON_FAINT,
                           actor=actor,
                           target=target,
                           fainted=animal)

        self.enqueue_event(eventnames.FRIEND_AHEAD_FAINTS,
                           actor=actor,
                           target=target,
                           fainted=animal)

        self.enqueue_event(eventnames.FRIEND_FAINTS,
                           actor=actor,
                           target=target,
                           fainted=animal)

        if not self.in_shop:
            # handle from perspective of unit which knocked unit out.
            self.enqueue_event(eventnames.KNOCK_OUT,
                               actor=target,
                               target=actor,
                               fainted=animal)


if __name__ == '__main__':
    while True:
        a = MessageAgent("base pack")
        print(animals[int(input("\nAnimal number: "))])
