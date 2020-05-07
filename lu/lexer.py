import re
from dataclasses import dataclass, field
from enum import Enum

from .types import TokenT


class TokenSpec(Enum):
    EOL = -1
    OP = 0
    LOC = 1
    NUM = 2
    IDENT = 3


@dataclass
class Token:
    spec: TokenSpec
    val: str


EOL_REGEXP = re.compile('^\n+$')
OP_REGEXP = re.compile('SET|DEF|ADD|SUB')
LOC_REGEXP = re.compile(r'^r[\d]+$')
NUM_REGEXP = re.compile(r'^[\d]+$')
IDENT_REGEXP = re.compile('^[a-zA-Z_]+$')
REGEXP_TO_TSPEC = {
    EOL_REGEXP: TokenSpec.EOL,
    OP_REGEXP: TokenSpec.OP,
    LOC_REGEXP: TokenSpec.LOC,
    NUM_REGEXP: TokenSpec.NUM,
    IDENT_REGEXP: TokenSpec.IDENT,
}


def _parse_token(token: str) -> TokenT:
    for t_regexp, t_spec in REGEXP_TO_TSPEC.items():
        match = t_regexp.match(token)

        if match is not None:
            return Token(spec=t_spec, val=token)

    else:
        msg = f'invalid token `{token}`.'
        raise Exception(msg)


def lexer(src: str):
    return [
        _parse_token(token)
        for ln in src.split('\n')
        for token in ln.split() + ['\n']
    ]
