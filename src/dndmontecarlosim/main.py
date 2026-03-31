import csv

from dndmontecarlosim.simple_combat_attack_simulation_runner import SimpleCombatAttackSimulationRunner
from dndmontecarlosim.sim_plan import SimpleSimulationPlan
from dndmontecarlosim.results_record import DamageRecord
from dndmodels import AttackActor, DefenseActor, DamageEvent
from dataclasses import asdict, fields
import json
import argparse
from csv import DictWriter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    new_command = subparsers.add_parser('new', help='Create a blank simulation plan file')
    run_command = subparsers.add_parser('run', help='Run a simulation')

    new_command.add_argument('new_filename', help='A new simulation plan file')
    run_command.add_argument('plan_filename', help='A simulation plan file')
    run_command.add_argument('-o', '--output_filename', default='sim_output.csv', help='The output file')
    run_command.add_argument('--repeat', default=1, type=int, help='The number of times to run the simulation')

    args = parser.parse_args()

    if not args.plan_filename:
        with open(args.new_filename, 'w') as f:
            plan = SimpleSimulationPlan(
                "Simple_Simulation_Plan_Name",
                "Simple_Simulation_Plan_Description",
                AttackActor(),
                DefenseActor(),
                DamageEvent(
                    "Damage_Name"
                )
            )
            plan_dict = asdict(plan)
            json.dump(plan_dict, f, indent=4)
    else:
        with open(args.plan_filename, 'r') as f:
            plan = SimpleSimulationPlan.from_json(json.load(f))
            runner = SimpleCombatAttackSimulationRunner(plan, args.repeat)
            runner.run_plan()

        with open(args.output_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[f.name for f in fields(DamageRecord)])
            writer.writeheader()
            writer.writerows([
                asdict(row) for row in runner.records
            ])