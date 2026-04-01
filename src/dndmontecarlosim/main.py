import csv

from dndmontecarlosim.simple_combat_attack_simulation_runner import SimpleCombatAttackSimulationRunner
from dndmontecarlosim.sim_plan import SimpleSimulationPlan
from dndmontecarlosim.results_record import DamageRecord
from dndmodels import AttackActor, DefenseActor, DamageEvent
from dataclasses import asdict, fields
import json
import argparse
from enum import StrEnum

class SimPlanMainArgs(StrEnum):
    NEW_FILENAME = "new_filename"
    PLAN_FILENAME = "plan_filename"
    OUTPUT_FILENAME = "output_filename"
    REPEAT = "repeat"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    new_command = subparsers.add_parser('new', help='Create a blank simulation plan file')
    run_command = subparsers.add_parser('run', help='Run a simulation')

    new_command.add_argument('new_filename', help='A new simulation plan file')
    run_command.add_argument('plan_filename', help='A simulation plan file')
    run_command.add_argument('-o', '--output_filename', default='sim_output.csv', help='The output file')
    run_command.add_argument('--repeat', default=1, type=int, help='The number of times to run the simulation')

    args = vars(parser.parse_args())

    if SimPlanMainArgs.PLAN_FILENAME not in args:
        with open(args[SimPlanMainArgs.NEW_FILENAME], 'w') as f:
            plan = SimpleSimulationPlan.get_template()
            plan_dict = asdict(plan)
            json.dump(plan_dict, f, indent=4)
    else:
        with open(args[SimPlanMainArgs.PLAN_FILENAME], 'r') as f:
            plan = SimpleSimulationPlan.from_json(json.load(f))
            runner = SimpleCombatAttackSimulationRunner(plan, args[SimPlanMainArgs.REPEAT])
            runner.run_plan()

        with open(args[SimPlanMainArgs.OUTPUT_FILENAME], 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[f.name for f in fields(DamageRecord)])
            writer.writeheader()
            writer.writerows([
                asdict(row) for row in runner.records
            ])