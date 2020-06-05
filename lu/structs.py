from dataclasses import dataclass
from enum import Enum


class TokenSpec(Enum):
    EOL = -1
    OP = 2
    LOC = 3
    NUM = 4
    IDENT = 5
    SYNTAX = 6


@dataclass
class Token:
    spec: TokenSpec
    val: str
