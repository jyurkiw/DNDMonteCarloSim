from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import StrEnum
from enum import IntEnum
import numpy as np


class RollCodeParts(StrEnum):
    d20 = "1d20"
    advantage = "2d20kh"
    disadvantage = "2d20kl"

class SimulationData(IntEnum):
    SIMULATION_NAME = 0
    ATTACKER_NAME = 1
    DEFENDER_NAME = 2
    ATTACK_NAME = 3
    SUCCESS = 4
    ROLL = 5
    TOTAL = 6
    DC = 7
    ATTACK_TYPE = 8
    DAMAGE_DONE = 9

class SimulationHeaders(StrEnum):
    SIMULATION_NAME = "Simulation Name"
    ATTACKER_NAME = "Attacker Name"
    DEFENDER_NAME = "Defender Name"
    ATTACK_NAME = "Attack Name"
    SUCCESS = "Success"
    ROLL = "Test Roll"
    TOTAL = "Test Total"
    DC = "DC"
    ATTACK_TYPE = "Attack Type"
    DAMAGE_DONE = "Damage Done"

simulation_field_header_datatypes = ['U50', 'U50', 'U50', 'U50', '?', 'i4', 'i4', 'i4', 'U50', 'i4']

simulation_data_csv_schema = np.dtype([
    (header.value, ftype)
    for header, ftype in zip(SimulationHeaders, simulation_field_header_datatypes)
])

csv_headers = ",".join([h.value for h in SimulationHeaders])

class SimulationStrings(StrEnum):
    ATTACK = "Attack"
    SAVING_THROW = "Saving Throw"