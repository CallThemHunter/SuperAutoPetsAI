from unittest import TestCase

from src.core.game_elements import Shop


class TestShop(TestCase):
    def test_buff(self):
        shop = Shop("base", 1)
        atk1 = shop[0].item.atk
        atk2 = shop[2].item.atk

        hp1 = shop[0].item.hp
        hp2 = shop[2].item.hp

        shop.buff(2, 1)

        self.assertTrue(atk1 + 2 == shop[0].item.atk)
        self.assertTrue(atk2 + 2 == shop[2].item.atk)
        self.assertTrue(hp1 + 1 == shop[0].item.hp)
        self.assertTrue(hp2 + 1 == shop[2].item.hp)

    def test_start_turn(self):
        shop = Shop("base", 6)

        self.assertTrue(len(shop.roster) == 7)
        shop.toggle_freeze(0)
        shop.toggle_freeze(2)
        shop.toggle_freeze(5)

        anim1 = shop[0].item
        anim2 = shop[2].item
        item = shop[5].item
        shop.start_turn()

        self.assertTrue(shop[0].item == anim1)
        self.assertTrue(shop[1].item == anim2)

        self.assertTrue(shop[5].item == item)

    def test_perm_buff(self):
        shop = Shop("base", 1)

        atk1 = shop[0].item.atk
        atk2 = shop[2].item.atk

        hp1 = shop[0].item.hp
        hp2 = shop[2].item.hp

        shop.perm_buff(2, 1)

        self.assertTrue(shop[0].item.atk == atk1 + 2)
        self.assertTrue(shop[2].item.atk == atk2 + 2)

        self.assertTrue(shop[0].item.hp == hp1 + 1)
        self.assertTrue(shop[2].item.hp == hp2 + 1)

        shop.reroll()

        atk1 = shop[0].item.atk
        atk2 = shop[2].item.atk

        hp1 = shop[0].item.hp
        hp2 = shop[2].item.hp

        shop.perm_buff(2, 1)

        self.assertTrue(shop[0].item.atk == atk1 + 2)
        self.assertTrue(shop[2].item.atk == atk2 + 2)

        self.assertTrue(shop[0].item.hp == hp1 + 1)
        self.assertTrue(shop[2].item.hp == hp2 + 1)

    def test_summon_level_unit(self):
        self.fail()

    def test_clear_unfrozen(self):
        self.fail()

    def test_clear(self):
        self.fail()

    def test_fill_shop(self):
        self.fail()

    def test_grow_shop(self):
        self.fail()

    def test_reroll(self):
        self.fail()

    def test_freeze(self):
        self.fail()
