import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from src.dndmontecarlosim.sim_methods import RollCodeFactory
from src.dndmontecarlosim.sim_methods import HitRollResult
from dndmodels.CombatantModel import CombatantModel, HitAttackEvent


class TestRollCodeFactoryStrMethods(unittest.TestCase):
    @staticmethod
    def get_attacker(sb=3, pb=4, eb=1, dc="1d8", mdb=2):
        return CombatantModel(
            name="Test Attacker",
            strength_bonus=sb,
            proficiency_bonus=pb,
            attacks=[
                HitAttackEvent(
                    name="Test Attack",
                    damage_code=dc,
                    enchantment_bonus=eb,
                    misc_damage_bonus=mdb
                )
            ]
        )

    @staticmethod
    def get_defender(ac=14):
        return CombatantModel(
            name="Test Defender",
            armor_class=ac
        )

    # get_success tests
    @parameterized.expand([
        (14, 15, False),
        (15, 15, True),
        (16, 15, True)
    ])
    def test_get_success(self, test_value, difficulty_class, expected):
        actual = RollCodeFactory.get_success(test_value, difficulty_class)
        self.assertEqual(actual, expected)

    # get_modifier_code tests
    @parameterized.expand([
        (-1, "-1"),
        (0, "+0"),
        (1, "+1")
    ])
    def test_get_modifier_code(self, modifier, expected):
        self.assertEqual(RollCodeFactory.get_modifier_code(modifier), expected)

    # get_d20_code tests (sanity test for now. [Ad/Dis]advanage later
    def test_get_get_d20_code(self):
        self.assertEqual(RollCodeFactory.get_d20_code(), "1d20")

    # get_hit_roll_code tests
    @parameterized.expand([
        (get_attacker(), "1d20+4+3+1"),
        (get_attacker(pb=-2), "1d20-2+3+1"),
        (get_attacker(pb=0, sb=-1), "1d20+0-1+1"),
        (get_attacker(pb=0, sb=-1, eb=-2), "1d20+0-1-2"),
    ])
    def test_get_hit_roll_code(self, attacker, expected):
        actual = RollCodeFactory.get_hit_roll_code(attacker, attacker.attacks[0])
        self.assertEqual(actual, expected)

    # get_damage_code tests
    @parameterized.expand([
        (get_attacker(), "1d8+3+2+1"),
        (get_attacker(dc="2d6"), "2d6+3+2+1"),
        (get_attacker(sb=-3), "1d8-3+2+1"),
        (get_attacker(mdb=-2), "1d8+3-2+1"),
        (get_attacker(eb=-1), "1d8+3+2-1"),
    ])
    def test_get_hit_damage_code(self, attacker, expected):
        actual = RollCodeFactory.get_hit_damage_code(attacker, attacker.attacks[0])
        self.assertEqual(actual, expected)

    # execute_hit_roll tests
    @parameterized.expand([
        (get_attacker(), get_defender(ac=17), HitRollResult(True, 10, 18, 17)),
        (get_attacker(), get_defender(ac=18), HitRollResult(True, 10, 18, 18)),
        (get_attacker(), get_defender(ac=19), HitRollResult(False, 10, 18, 19)),
    ])
    def test_execute_hit_roll(self, attacker, defender, hit):
        with patch('src.dndmontecarlosim.sim_methods.Roll') as MockRoll:
            roll = MagicMock()
            roll.total = 18
            roll.rolls = [10]
            MockRoll.return_value = roll
            actual = RollCodeFactory.execute_hit_roll(attacker, attacker.attacks[0], defender)
            self.assertEqual(actual, hit)


if __name__ == '__main__':
    unittest.main()
