from dataclasses import dataclass, field
from .structs import TokenSpec
from .types import List


@dataclass
class SigVar:
    specs: List[TokenSpec] = field(default_factory=list)
    is_opt: bool = False


class Op:
    SIG_DEF = []

    def __init__(self):
        self.name = None
        self.tokens = []
        self.args = []
        self.sig = None

    def __repr__(self):
        return f'Op(name={self.name})'

    def copy_state_of(self, other):
        self.__dict__ = other.__dict__.copy()


class Procedure:
    SIG_DEF = None

    def __init__(self):
        self.name = None
        self.tokens = []
        self.args = []
        self.body = []
        self.ops = []
        self.sig = None

    def __repr__(self):
        return f'Procedure(name={self.name})'
