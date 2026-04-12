from dndmontecarlosim import constants
from dndmontecarlosim.sim_plan import get_simulation_plan_template

from dndmontecarlosim.sim_plan import SimulationPlan
from dndmontecarlosim.sim_methods import RollCodeFactory
from dndmontecarlosim import constants as simconstants
from dndmodels.CombatantModel import HitAttackEvent
import numpy as np
import numpy.typing as npt

class RunException(Exception):
    pass

def run(simulation_name: str, simulation_plan: SimulationPlan) -> npt.NDArray[np.void]:
    """Run the Simulation Plan"""
    attacker = simulation_plan.attacker
    attack = attacker.attacks[0]
    defender = simulation_plan.defender

    simulation_data = np.empty(simulation_plan.iterations, dtype=simconstants.simulation_data_csv_schema)

    if isinstance(attack, HitAttackEvent):
        attack_type = simconstants.SimulationStrings.ATTACK
        attack_code = RollCodeFactory.get_hit_roll_code(attacker, attack)
        damage_code = RollCodeFactory.get_hit_damage_code(attacker, attack)
    else:
        raise RunException(f"Attack {attack.name} was determined to be a {type(attack)} when HitAttackEvent was expected.")

    for i in range(simulation_plan.iterations):
        hit_roll = RollCodeFactory.execute_hit_roll(attacker, attack, defender)
        if hit_roll.success:
            damage = RollCodeFactory.execute_damage_roll(attacker, attack)
        else:
            damage = 0

        # Set simulation data for this iteration
        simulation_data[i][simconstants.SimulationHeaders.SIMULATION_NAME.value] = simulation_name
        simulation_data[i][simconstants.SimulationHeaders.ATTACKER_NAME.value] = attacker.name
        simulation_data[i][simconstants.SimulationHeaders.DEFENDER_NAME.value] = defender.name
        simulation_data[i][simconstants.SimulationHeaders.ATTACK_NAME.value] = attack.name
        simulation_data[i][simconstants.SimulationHeaders.SUCCESS.value] = hit_roll.success
        simulation_data[i][simconstants.SimulationHeaders.ROLL.value] = hit_roll.roll
        simulation_data[i][simconstants.SimulationHeaders.TOTAL.value] = hit_roll.total
        simulation_data[i][simconstants.SimulationHeaders.DC.value] = defender.armor_class
        simulation_data[i][simconstants.SimulationHeaders.ATTACK_TYPE.value] = attack_type

    return simulation_data

def save(simulation_data: npt.NDArray[np.void], file_path: str) -> None:
    np.savetxt(
        file_path,
        simulation_data,
        delimiter=",",
        header=simconstants.csv_headers,
        comments='',
        fmt="%s"
    )
