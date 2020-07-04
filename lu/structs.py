from copy import copy
from dataclasses import dataclass


class Stack:

    def __init__(self):
        self._cont = []

    def __repr__(self):
        return repr(self._cont)

    @property
    def elements(self):
        return copy(self._cont)

    def clear(self):
        self._cont = []

    def push(self, el):
        self._cont.append(el)

    def peek(self):
        return self._cont[-1] if self._cont else None

    def pop(self):
        return self._cont.pop() if self._cont else None

    def pop_all(self):
        rv = self.elements
        self.clear()
        return rv


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
