from dndmodels import Situation, Resistance, DamageType
from random import randint
from .results_record import DamageRecord
from .sim_plan import SimpleSimulationPlan
from uuid import uuid4


class SimpleCombatAttackSimulationRunner(object):
    def __init__(self, simulation_plan: SimpleSimulationPlan, repeats: int):
        self.simulation_plan = simulation_plan
        self.repeats = repeats
        self.records = []

    def run_plan(self):
        sim_name = str(uuid4())

        # Calculate total attack bonus
        total_attack_bonus = (self.simulation_plan.attacker.proficiency
            + self.simulation_plan.attacker.stat_bonus
            + self.simulation_plan.attacker.enchantment)

        for round_number in range(1, self.repeats + 1):
            # Determine advantage/disadvantage
            if self.simulation_plan.attacker.situation == Situation.NORMAL:
                roll = randint(1, 20)
            elif self.simulation_plan.attacker.situation == Situation.ADVANTAGE:
                roll = max(randint(1, 20), randint(1, 20))
            else:
                roll = min(randint(1, 20), randint(1, 20))

            # Determine hit or miss
            if roll + total_attack_bonus < self.simulation_plan.defender.armor_class:
                # Add the result record to the record list
                record = DamageRecord(
                    sim_name,
                    round_number,
                    "miss",
                    "miss",
                    0
                )
                self.records.append(record)
            else:
                # Calculate base damage
                damage = (sum([
                        randint(1, self.simulation_plan.damage.sides)
                        for _ in range(self.simulation_plan.damage.number)])
                    + self.simulation_plan.damage.bonus)

                # Calculate critical hits
                if roll == 20:
                    damage += (sum([
                        randint(1, self.simulation_plan.damage.sides)
                        for _ in range(self.simulation_plan.damage.number)]))

                # Determine if resistance or vulnerability applies and apply as appropriate
                if (self.simulation_plan.defender.resistance != Resistance.NORMAL
                    and self.simulation_plan.defender.resistance_type == self.simulation_plan.damage.type):
                    if self.simulation_plan.defender.resistance == Resistance.RESISTANCE:
                        damage = round(damage/2)
                    elif self.simulation_plan.defender.resistance == Resistance.VULNERABILITY:
                        damage = damage * 2
                    else:
                        damage = 0

                # Add the result record to the record list
                record = DamageRecord(
                    sim_name,
                    round_number,
                    str(self.simulation_plan.damage.type),
                    self.simulation_plan.damage.get_damage_code(),
                    damage
                )
                self.records.append(record)
