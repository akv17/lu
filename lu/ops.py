from .core import Op, VarDef
from .structs import TokenSpec


class SetOp(Op):
    SIG_DEF = [
        VarDef(specs=[TokenSpec.LOC, TokenSpec.IDENT], allow_unset=True),
        VarDef(specs=[TokenSpec.LOC, TokenSpec.IDENT, TokenSpec.CONST]),
    ]

    def execute(self, ctx):
        src, dst = self.sig.bind(ctx)

        if src.sig.spec == TokenSpec.LOC:
            ctx.set_reg(src.sig.val, dst.val)

        elif src.sig.spec == TokenSpec.IDENT:
            ctx.set_mem(src.sig.val, dst.val)


class AddOp(Op):
    SIG_DEF = [
        VarDef(specs=[TokenSpec.LOC, TokenSpec.IDENT]),
        VarDef(specs=[TokenSpec.LOC, TokenSpec.IDENT, TokenSpec.CONST]),
    ]


class CallOp(Op):
    SIG_DEF = [VarDef(specs=[TokenSpec.IDENT])]


OPS = {
    'SET': SetOp,
    'ADD': AddOp,
    'CALL': CallOp
}


__all__ = ['OPS']
