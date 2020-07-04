from .core import Op, SigVar
from .structs import TokenSpec


class SetOp(Op):
    SIG_DEF = [
        SigVar(specs=[TokenSpec.LOC, TokenSpec.IDENT]),
        SigVar(specs=[TokenSpec.LOC, TokenSpec.IDENT, TokenSpec.NUM]),
    ]


class AddOp(Op):
    SIG_DEF = [
        SigVar(specs=[TokenSpec.LOC, TokenSpec.IDENT]),
        SigVar(specs=[TokenSpec.LOC, TokenSpec.IDENT, TokenSpec.NUM]),
    ]


OPS = {'SET': SetOp, 'ADD': AddOp}


__all__ = ['OPS']
