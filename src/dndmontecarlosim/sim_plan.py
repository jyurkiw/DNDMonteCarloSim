from dataclasses import dataclass
from dndmodels import AttackActor, DefenseActor, DamageEvent, Situation, Resistance, DamageType


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
        attacker = AttackActor(
            proficiency=int(parsed_json["attacker"]["proficiency"]),
            stat_bonus=int(parsed_json["attacker"]["stat_bonus"]),
            enchantment=int(parsed_json["attacker"]["enchantment"]),
            situation=Situation(parsed_json["attacker"]["situation"]),
        )
        defender = DefenseActor(
            armor_class=int(parsed_json["defender"]["armor_class"]),
            resistance=Resistance(parsed_json["defender"]["resistance"]),
            resistance_type=DamageType(parsed_json["defender"]["resistance_type"]),
        )
        damage = DamageEvent(
            source_name=parsed_json["damage"]["source_name"],
            number=int(parsed_json["damage"]["number"]),
            sides=int(parsed_json["damage"]["sides"]),
            bonus=int(parsed_json["damage"]["bonus"]),
            type=DamageType(parsed_json["damage"]["type"]),
        )
        plan = SimpleSimulationPlan(
            name=parsed_json["name"],
            description=parsed_json["description"],
            attacker=attacker,
            defender=defender,
            damage=damage,
            rounds=int(parsed_json["rounds"]),
        )
        return plan