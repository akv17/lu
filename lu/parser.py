from copy import copy
from dataclasses import dataclass, field

from .types import TokenT, List
from .structs import Token, TokenSpec


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


@dataclass
class Procedure:
    name: str
    tokens: list = field(default_factory=list)


def parse(tokens: List[TokenT]):
    active_stack = Stack()
    done_stack = Stack()

    for token in tokens:
        if token.spec is TokenSpec.OP and token.val == 'DEF':
            prcd = Procedure(name=token.val)
            active_stack.push(prcd)

        elif token.spec is TokenSpec.OP and token.val == 'END':
            prcd = active_stack.pop()

            if prcd is None:
                msg = f'got END with no DEF.'
                raise Exception(msg)

            done_stack.push(prcd)

        else:
            prcd = active_stack.peek()

            if prcd is None:
                msg = f'got no active procedure.'
                raise Exception(msg)

            prcd.tokens.append(token)

    return done_stack.elements
