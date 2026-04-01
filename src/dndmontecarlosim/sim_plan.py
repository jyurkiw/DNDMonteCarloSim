from dataclasses import dataclass
from dndmodels import AttackActor
from dndmodels import DefenseActor
from dndmodels import DamageEvent
from dndmodels import AttackerConstants
from dndmodels import DefenderConstants
from constants import SimPlanConstants


@dataclass
class SimpleSimulationPlan(object):
    name: str
    description: str
    attacker: AttackActor
    defender: DefenseActor
    damage: DamageEvent
    rounds: int = 3

    @staticmethod
    def from_json(parsed_json: dict):
        plan = SimpleSimulationPlan(
            name=parsed_json[SimPlanConstants.NAME],
            description=parsed_json[SimPlanConstants.DESCRIPTION],
            attacker=AttackActor.from_json(parsed_json[AttackerConstants.ATTACKER]),
            defender=DefenseActor.from_json(parsed_json[DefenderConstants.DEFENDER]),
            damage=DamageEvent.from_json(parsed_json[SimPlanConstants.DAMAGE]),
            rounds=int(parsed_json[SimPlanConstants.ROUNDS]),
        )
        return plan