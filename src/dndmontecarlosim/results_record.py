from dataclasses import dataclass


@dataclass(frozen=True)
class DamageRecord(object):
    name: str
    round_number: int
    damage_type: str
    damage_code: str
    total: int

    def get_row(self):
        return [self.round_number, self.damage_type, self.damage_code, self.total]