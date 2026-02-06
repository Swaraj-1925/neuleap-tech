import json
from enum import Enum
from typing import Dict, List

DATA_FILE = "interns.json"

def generate_intern_id(len_interns:int)-> str:
    return f"INT{len_interns + 1:03d}"

class Status(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    COMPLETED = "Completed"

