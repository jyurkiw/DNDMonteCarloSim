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
    """
    Defines a simulation plan for a single attacker against a single defender.

    This class encapsulates all necessary components for running a single-attacker
    simulation, including the attacker actor, defender actor, damage event details,
    and the number of simulation rounds.
    """
    name: str
    description: str
    attacker: AttackActor
    defender: DefenseActor
    damage: DamageEvent
    rounds: int = 3

    @staticmethod
    def from_json(parsed_json: dict):
        """
        Constructs a SingleAttackerSimulationPlan instance from a parsed JSON dictionary.

        Args:
            parsed_json: A dictionary containing the simulation plan data, keyed by
                         constants defined in SimPlanConstants, AttackerConstants,
                         and DefenderConstants.

        Returns:
            SingleAttackerSimulationPlan: A fully initialized simulation plan object.
        """
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
        """
        Creates a default, template instance of a SingleAttackerSimulationPlan.

        This method initializes the plan with default actors and a default damage event
        based on predefined constants.

        Returns:
            SingleAttackerSimulationPlan: A default simulation plan instance.
        """
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