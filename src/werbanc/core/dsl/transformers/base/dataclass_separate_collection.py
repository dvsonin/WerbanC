from typing import Any
from dataclasses import dataclass

@dataclass
class Variable:
    name: str
    value: Any