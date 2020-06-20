from dataclasses import dataclass


class TokenSpec:
    EOL = 'EOL'
    OP = 'OP'
    LOC = 'LOC'
    NUM = 'NUM'
    IDENT = 'IDENT'
    SYNTAX = 'SYNTAX'
    DEF = 'DEF'
    END = 'END'


@dataclass
class Token:
    spec: TokenSpec
    val: str
    line_num: int = -1
