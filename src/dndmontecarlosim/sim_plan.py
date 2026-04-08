import warnings
from dataclasses import dataclass

from dndmodels import AttackActor
from dndmodels import DefenseActor
from dndmodels import DamageEvent
from dndmodels import AttackerConstants
from dndmodels import DefenderConstants
from .constants import SimPlanConstants


@dataclass
class SingleAttackerSimulationPlan(object):
    name: str
    description: str
    attacker: AttackActor
    defender: DefenseActor
    damage: DamageEvent
    rounds: int = 3

    @staticmethod
    def from_json(parsed_json: dict):
        plan = SingleAttackerSimulationPlan(
            name=parsed_json[SimPlanConstants.NAME],
            description=parsed_json[SimPlanConstants.DESCRIPTION],
            attacker=parsed_json[AttackerConstants.ATTACKER],
            defender=DefenseActor.from_json(parsed_json[DefenderConstants.DEFENDER]),
            damage=DamageEvent.from_json(parsed_json[SimPlanConstants.DAMAGE]),
            rounds=int(parsed_json[SimPlanConstants.ROUNDS]),
        )
        return plan

    @staticmethod
    def get_template():
        return SingleAttackerSimulationPlan(
            SimPlanConstants.TEMPLATE_PLAN_NAME,
            SimPlanConstants.TEMPLATE_PLAN_DESCRIPTION,
            AttackActor(),
            DefenseActor(),
            DamageEvent(
                SimPlanConstants.DAMAGE_NAME
            )
        )

@warnings.deprecated("SimpleSimulationPlan is deprecated. Use SingleAttackerSimulationPlan instead")
@dataclass
class SimpleSimulationPlan(SingleAttackerSimulationPlan):
    pass