from copy import copy

from .types import TokenT, List
from .structs import TokenSpec
from .procedure import Procedure
from .op import Op


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


class OpParser:

    def _assert_not_empty(self, op, toks):
        if not toks:
            msg = f'cannot compile empty op `{op}`.'
            raise Exception(msg)

    def _assert_name(self, op, tok):
        if tok.spec != TokenSpec.OP:
            msg = f'got invalid op def `{op}`.'
            raise Exception(msg)

        return tok

    def _split_tokens(self, toks):
        name_tok = toks[0]
        arg_toks = toks[1:]
        return name_tok, arg_toks

    def __call__(self, op):
        toks = op.tokens
        self._assert_not_empty(op, toks)

        name_tok, arg_toks = self._split_tokens(toks)
        name_tok = self._assert_name(op, name_tok)

        op.name = name_tok
        op.args = arg_toks
        return op


class ProcedureParser:

    def _assert_not_empty(self, proc, toks):
        if not toks:
            msg = f'cannot compile empty procedure `{proc}`.'
            raise Exception(msg)

    def _assert_name(self, proc, tok):
        if tok.spec != TokenSpec.IDENT:
            msg = f'got invalid sig def `{proc}`'
            raise Exception(msg)

        return tok

    def _split_tokens(self, toks):
        # relying on pre-made `toks` non empty check.
        name_tok = toks[0]
        sig_toks = []
        body_toks = []
        seen_eol = False

        for i, tok in enumerate(toks[1:]):
            if tok.spec == TokenSpec.EOL:
                seen_eol = True

            elif not seen_eol:
                sig_toks.append(tok)

            else:
                # compensate one for name token.
                body_toks = toks[i + 1:]
                break

        return name_tok, sig_toks, body_toks

    def _parse_args(self, toks):
        assert len(toks) >= 2, 'got invalid sig def'
        assert toks[0].spec == TokenSpec.SYNTAX and toks[0].val == '(', 'got invalid sig def'
        assert toks[-1].spec == TokenSpec.SYNTAX and toks[-1].val == ')', 'got invalid sig def'

        args = []
        state = {'seen_arg': False, 'seen_sep': True}

        for tok in toks[1:-1]:
            if tok.spec != TokenSpec.IDENT and tok.val != ',':
                raise Exception('got invalid sig def')

            if tok.spec == TokenSpec.IDENT:
                if not state['seen_sep']:
                    raise Exception('got invalid sig def')

                args.append(tok)
                state['seen_sep'] = False
                state['seen_arg'] = True

            elif tok.val == ',':
                if not state['seen_arg']:
                    raise Exception('got invalid sig def')

                state['seen_sep'] = True
                state['seen_arg'] = False

        args = {t.val: t for t in args}
        return args

    def __call__(self, proc):
        toks = proc.tokens
        self._assert_not_empty(proc, toks)
        name_tok, sig_toks, body_toks = self._split_tokens(toks)

        name_tok = self._assert_name(proc, name_tok)
        args_toks = self._parse_args(sig_toks)

        proc.name = name_tok
        proc.args = args_toks
        proc.body = body_toks
        return proc


class Parser:

    def __init__(self, proc_parser, op_parser):
        self._proc_parser = proc_parser
        self._op_parser = op_parser

    def _extract_procs(self, tokens: List[TokenT]):
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

        procs = done_stack.elements
        active_stack.clear()
        done_stack.clear()
        return procs

    def _extract_ops(self, tokens: List[TokenT]):
        ops = []
        toks_stack = Stack()

        for tok in tokens:
            if tok.spec == TokenSpec.EOL:
                if toks_stack.elements:
                    op = Op()
                    op.tokens = toks_stack.pop_all()
                    ops.append(op)

            else:
                toks_stack.push(tok)

        toks_stack.clear()
        return ops

    def _parse_proc(self, proc):
        proc = self._proc_parser(proc)
        ops = self._extract_ops(proc.body)
        ops = [self._op_parser(op) for op in ops]
        proc.ops = ops
        return proc

    def __call__(self, tokens: List[TokenT]):
        procs = self._extract_procs(tokens)
        procs = [self._parse_proc(p) for p in procs]
        return procs
