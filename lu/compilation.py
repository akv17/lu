from .core import Op
from .ops import OPS


class Signature:

    def __init__(self, sig_def, args):
        self._def = sig_def
        self._args = args

        if self._def is not None:
            self._assert_sig_def(self._def)

    def _assert_sig_def(self, sig_def):
        for def_arg, actual_arg in zip(sig_def, self._args):
            if not def_arg.is_opt and actual_arg is None:
                msg = f'missing arg {actual_arg} of sig {sig_def}.'
                raise Exception(msg)

            if actual_arg.spec not in def_arg.specs:
                msg = f'got invalid arg {actual_arg} of sig {sig_def}.'
                raise Exception(msg)

    def bind(self, ctx):
        pass


class Compiler:

    def compile_obj(self, obj):
        if isinstance(obj, Op):
            op_name = obj.name.val
            if op_name not in OPS:
                msg = f'got unknown op `{op_name}`.'
                raise Exception(msg)

            # spawn concrete implementation of op.
            concrete_obj = OPS[op_name]()
            concrete_obj.copy_state_of(obj)
            obj = concrete_obj

        sig = Signature(sig_def=obj.SIG_DEF, args=obj.args)
        obj.sig = sig
        return obj

    def compile_proc(self, proc):
        proc = self.compile_obj(proc)
        proc.ops = [self.compile_obj(op) for op in proc.ops]
        return proc
