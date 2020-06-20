from .structs import TokenSpec


class ProcedureCompiler:

    def _assert_not_empty(self, toks):
        if not toks:
            msg = 'cannot compile empty procedure.'
            raise Exception(msg)

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

    def _set_name(self, proc, tok):
        if tok.spec != TokenSpec.IDENT:
            raise Exception('got invalid sig def')

        proc.name = tok

    def _compile_sig(self, proc, toks):
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

        proc.args = args

    def _compile_body(self, proc, toks):
        pass

    def __call__(self, proc):
        toks = proc.tokens
        self._assert_not_empty(toks)
        name_tok, sig_toks, body_toks = self._split_tokens(toks)
        self._set_name(proc, name_tok)
        self._compile_sig(proc, sig_toks)
        self._compile_body(proc, body_toks)


class Procedure:
    _COMPILER_TYPE = ProcedureCompiler

    def __init__(self):
        self.name = None
        self.tokens = []
        self.args = []
        self._compiler = self._COMPILER_TYPE()

    def __repr__(self):
        return f'Procedure(name={self.name})'

    def compile(self):
        self._compiler(self)