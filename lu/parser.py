from copy import copy

from .types import TokenT, List
from .structs import TokenSpec
from .procedure import Procedure


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


def parse(tokens: List[TokenT]):
    active_stack = Stack()
    done_stack = Stack()

    for token in tokens:
        if token.spec == TokenSpec.DEF:
            proc = Procedure()
            active_stack.push(proc)

        elif token.spec == TokenSpec.END:
            proc = active_stack.pop()

            if proc is None:
                msg = f'got END with no DEF.'
                raise Exception(msg)

            done_stack.push(proc)

        else:
            proc = active_stack.peek()

            if proc is None:
                msg = f'got no active procedure.'
                raise Exception(msg)

            proc.tokens.append(token)

    return done_stack.elements
