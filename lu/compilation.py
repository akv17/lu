from .core import Signature
from .ops import OPS


class Compiler:

    def _set_sig(self, obj):
        sig = Signature(sig_def=obj.SIG_DEF, args=obj.args)
        obj.sig = sig
        return obj

    def compile_op(self, op):
        op_name = op.name.val
        if op_name not in OPS:
            msg = f'got unknown op `{op_name}`.'
            raise Exception(msg)

        # spawn concrete implementation of op.
        concrete_op = OPS[op_name]()
        concrete_op.copy_state_of(op)
        op = concrete_op
        op = self._set_sig(op)
        return op

    def compile_proc(self, proc):
        proc.ops = [self.compile_op(op) for op in proc.ops]
        proc = self._set_sig(proc)
        return proc

    def compile_procs(self, procs):
        return [self.compile_proc(p) for p in procs]
