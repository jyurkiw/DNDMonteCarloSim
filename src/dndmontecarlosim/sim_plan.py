from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dndmodels.CombatantModel import CombatantModel, HitAttackEvent, SaveAttackEvent


@dataclass_json
@dataclass(frozen=True)
class SimulationPlan(object):
    attacker: CombatantModel
    defender: CombatantModel

    # Simulation Run Variables
    iterations: int = 500


def get_simulation_plan_template() -> SimulationPlan:
    return SimulationPlan(
        attacker=CombatantModel(
            name="Attacker Template",
            attacks=[
                HitAttackEvent(name="Hit Roll Attack Template"),
                SaveAttackEvent(name="Saving Throw Attack Template")
            ]
        ),
        defender=CombatantModel(
            name="Defender Template"
        ),
    )
