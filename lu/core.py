from dataclasses import dataclass, field
from .structs import TokenSpec
from .types import List, Any


@dataclass
class VarDef:
    specs: List[TokenSpec] = field(default_factory=list)
    allow_unset: bool = False
    is_opt: bool = False


@dataclass
class VarSig:
    spec: TokenSpec
    val: Any = None
    allow_unset: bool = False
    is_const: bool = False


@dataclass
class Var:
    sig: VarSig
    val: Any = None


def create_var(token, var_def=None):
    allow_unset = var_def.allow_unset if var_def is not None else False
    sig = VarSig(spec=token.spec, val=token.val, allow_unset=allow_unset)

    # set sig vals computed in compile-time.
    if token.const_val is not None:
        sig.val = token.const_val

    var = Var(sig=sig)
    if token.spec == TokenSpec.CONST:
        var.val = token.const_val
        sig.is_const = True

    return var


class Signature:

    def __init__(self, sig_def, args):
        self._args = args
        self.sig_def = sig_def
        self.vars = self._create_vars()

    def _create_vars(self):
        if self.sig_def is None:
            return [create_var(arg) for arg in self._args]

        vars_ = []
        for arg_def, arg in zip(self.sig_def, self._args):
            if not arg_def.is_opt and arg is None:
                msg = f'missing arg {arg} of sig {self.sig_def}.'
                raise Exception(msg)

            if arg.spec not in arg_def.specs:
                msg = f'got invalid arg {arg} of sig {self.sig_def}.'
                raise Exception(msg)

            var = create_var(token=arg, var_def=arg_def)
            vars_.append(var)

        return vars_

    def bind(self, ctx):
        for var in self.vars:
            if var.sig.allow_unset:
                continue

            elif var.sig.spec == TokenSpec.LOC:
                var.val = ctx.get_reg(var.sig.val)

            elif var.sig.spec == TokenSpec.IDENT:
                var.val = ctx.get_mem_by_name(var.sig.val)

        return self.vars


class Executable:
    SIG_DEF = None

    def __init__(self):
        self.name = None
        self.tokens = []
        self.args = []
        self.sig = None

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name.val})'

    def execute(self, ctx):
        print(f'EXEC {self}')
        pass


class Op(Executable):

    def copy_state_of(self, other):
        self.__dict__ = other.__dict__.copy()


class Procedure(Executable):
    SIG_DEF = None

    def __init__(self):
        super().__init__()
        self.body = []
        self.ops = []

    def execute(self, ctx):
        print(f'EXEC {self}')
        for op in self.ops:
            op.execute(ctx)
