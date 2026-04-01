from dataclasses import dataclass
from dndmodels import AttackActor
from dndmodels import DefenseActor
from dndmodels import DamageEvent
from dndmodels import AttackerConstants
from dndmodels import DefenderConstants
from .constants import SimPlanConstants


@dataclass
class SimpleSimulationPlan(object):
    name: str
    description: str
    attackers: list[AttackActor]
    defender: DefenseActor
    damage: DamageEvent
    rounds: int = 3

    @staticmethod
    def from_json(parsed_json: dict):
        plan = SimpleSimulationPlan(
            name=parsed_json[SimPlanConstants.NAME],
            description=parsed_json[SimPlanConstants.DESCRIPTION],
            attackers=[AttackActor.from_json(attacker) for attacker in parsed_json[AttackerConstants.ATTACKERS]],
            defender=DefenseActor.from_json(parsed_json[DefenderConstants.DEFENDER]),
            damage=DamageEvent.from_json(parsed_json[SimPlanConstants.DAMAGE]),
            rounds=int(parsed_json[SimPlanConstants.ROUNDS]),
        )
        return plan

    @staticmethod
    def get_template():
        return SimpleSimulationPlan(
            SimPlanConstants.TEMPLATE_PLAN_NAME,
            SimPlanConstants.TEMPLATE_PLAN_DESCRIPTION,
            [AttackActor()],
            DefenseActor(),
            DamageEvent(
                SimPlanConstants.DAMAGE_NAME
            )
        )