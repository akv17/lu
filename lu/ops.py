


class SetOp(Op):
    SIG_DEF = [
        SigVar(specs=[TokenSpec.LOC, TokenSpec.IDENT]),
        SigVar(specs=[TokenSpec.LOC, TokenSpec.IDENT, TokenSpec.NUM]),
    ]
