import re

from .types import TokenT, List
from .structs import Token, TokenSpec

SYNTAX_TOKENS = {'(', ')', ','}
TSPEC_REGEXP_MAP = {
    re.compile('^\n+$'): TokenSpec.EOL,
    re.compile(f'[{"".join(SYNTAX_TOKENS)}]'): TokenSpec.SYNTAX,
    re.compile(r'DEF'): TokenSpec.DEF,
    re.compile(r'END'): TokenSpec.END,
    re.compile('CALL|SET|ADD|SUB|MUL|DIV'): TokenSpec.OP,
    re.compile(r'^r[\d]+$'): TokenSpec.LOC,
    re.compile(r'^[\d]+$'): TokenSpec.CONST,
    re.compile('^[a-zA-Z_]+$'): TokenSpec.IDENT,
}
MAIN_PROCEDURE_HEADER = 'DEF __MAIN__ ()'
MAIN_PROCEDURE_TAIL = 'END'


class Lexer:

    def __init__(
        self,
        syntax_tokens: set,
        tspec_regexp_map: dict,
    ):
        self._syntax_tokens = syntax_tokens
        self._tspec_regexp_map = tspec_regexp_map

    def _create_token_obj(self, t_str: str):
        for t_regexp, t_spec in self._tspec_regexp_map.items():
            match = t_regexp.match(t_str)

            if match is not None:
                tok = Token(spec=t_spec, val=t_str)

                if t_spec == TokenSpec.CONST:
                    tok.const_val = int(tok.val)

                elif t_spec == TokenSpec.LOC:
                    tok.const_val = int(tok.val.replace('r', ''))

                return tok

        else:
            msg = f'invalid token `{t_str}`.'
            raise Exception(msg)

    def _parse_word(self, word: str):
        synt_tokens = self._syntax_tokens

        w_start = 0
        for ch in word:
            if ch not in synt_tokens:
                break
            w_start += 1

        le_synt_chars = list(word[:w_start])
        word = word[w_start:]

        w_end = len(word)
        for ch in word[::-1]:
            if ch not in synt_tokens:
                break
            w_end -= 1

        ri_synt_chars = list(word[w_end:])
        word = word[:w_end]

        tokens = le_synt_chars + [word] + ri_synt_chars
        tokens = [self._create_token_obj(t) for t in tokens if t]
        return tokens

    def _wrap_main_proc(self, tokens):
        header_tokens = self(MAIN_PROCEDURE_HEADER, _wrap_guard=True)
        # exclude the very last EOL.
        tail_tokens = self(MAIN_PROCEDURE_TAIL, _wrap_guard=True)[:-1]
        return header_tokens + tokens + tail_tokens

    def __call__(self, src: str, _wrap_guard=False) -> List[TokenT]:
        # TODO: track src linenum
        tokens = []

        for ln in src.split('\n'):
            for word in ln.split(' ') + ['\n']:
                tokens.extend(self._parse_word(word))

        if not _wrap_guard:
            tokens = self._wrap_main_proc(tokens)

        return tokens
