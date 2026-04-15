from .sim_plan import SimulationPlan
from dndmodels.CombatantModel import CombatantModel
from dndmodels.CombatantModel import HitAttackEvent

from collections import namedtuple

from roller import Roll

import dndmodels.constants as dmconst

HitRollResult = namedtuple('HitRollResult', ('success', 'roll', 'total', 'dc'))

class RollCodeFactory(object):
    @staticmethod
    def get_success(test_value, difficulty_class) -> bool:
        return test_value >= difficulty_class

    @staticmethod
    def get_modifier_code(modifier: int) -> str:
        if modifier < 0:
            return f"-{abs(modifier)}"
        else:
            return f"+{modifier}"

    @staticmethod
    def get_d20_code() -> str:
        return "1d20"

    @staticmethod
    def get_hit_roll_code(attacker: CombatantModel, attack: HitAttackEvent) -> str:
        """Get a hit roll code.
        Example Code: 1d20+2+3+1
        Example Breakdown:
            1d20: basic roll mechanic. No advantage or disadvantage.
            +2: proficiency bonus
            +3: stat bonus
            +1: weapon enchantment bonus
        """
        return "".join([
            RollCodeFactory.get_d20_code(),
            RollCodeFactory.get_modifier_code(attacker.proficiency_bonus),
            RollCodeFactory.get_modifier_code(attacker.get_stat_bonus(attack.bonus_stat)),
            RollCodeFactory.get_modifier_code(attack.enchantment_bonus),
        ])

    @staticmethod
    def is_critical_hit(attack: HitAttackEvent, attack_roll: int) -> bool:
        """Returns True if the hit was a crit."""
        return attack_roll in attack.crit_numbers

    @staticmethod
    def get_hit_damage_code(attacker: CombatantModel, attack: HitAttackEvent, is_crit: bool = False) -> str:
        """Get a damage code.
        Example Code: 1d8+3+1+1
        Example Breakdown:
            1d8: longsword damage
            +3: stat bonus
            +1: miscellaneous damage bonus
            +1: enchantment bonus
        """
        return "".join([
            attack.damage_code,
            RollCodeFactory.get_modifier_code(attacker.get_stat_bonus(attack.bonus_stat)),
            RollCodeFactory.get_modifier_code(attack.misc_damage_bonus),
            RollCodeFactory.get_modifier_code(attack.enchantment_bonus),
            f"+{attack.crit_damage_code}" if is_crit else ""
        ])

    @staticmethod
    def execute_hit_roll(attacker: CombatantModel, attack: HitAttackEvent, target: CombatantModel) -> HitRollResult:
        """Roll to hit.
        For now, just return the hit/miss status.
        """
        hit_code = RollCodeFactory.get_hit_roll_code(attacker, attack)
        armor_class = target.armor_class
        roll = Roll(hit_code)

        return HitRollResult(RollCodeFactory.get_success(roll.total, armor_class), roll.rolls[0].details[0], roll.total, target.armor_class)

    @staticmethod
    def execute_damage_roll(attacker: CombatantModel, attack: HitAttackEvent, is_crit: bool = False) -> int:
        """Roll damage.
        For now, just return damage for weapon attacks.
        """
        damage_code = RollCodeFactory.get_hit_damage_code(attacker, attack, is_crit)
        damage = Roll(damage_code).total

        return damage