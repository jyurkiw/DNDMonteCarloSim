import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from src.dndmontecarlosim.sim_methods import RollCodeFactory
from src.dndmontecarlosim.sim_methods import HitRollResult
from dndmodels.CombatantModel import CombatantModel, HitAttackEvent

from roller import RollEntry

def getMockRoll(code, total_static=0, *roll_entries):
    mr = MagicMock()
    mr.code = code
    mr.rolls = roll_entries
    mr.total_static = total_static
    mr.total = sum([r for i in mr.rolls for r in i.details]) + mr.total_static

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
        (get_attacker(pb=0, sb=-1, eb=-2), "1d20+0-1-2")
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
        (get_attacker(), "1d8+3+2+1+1d6", True)
    ])
    def test_get_hit_damage_code(self, attacker, expected, crit=False):
        actual = RollCodeFactory.get_hit_damage_code(attacker, attacker.attacks[0], crit)
        self.assertEqual(actual, expected)

    # execute_hit_roll tests
    @parameterized.expand([
    ])
    def test_execute_hit_roll(self, attacker, defender, expected):
        actual = RollCodeFactory.execute_hit_roll(attacker, attacker.attacks[0], defender)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
