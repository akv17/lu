from .lexing import Lexer, SYNTAX_TOKENS, TSPEC_REGEXP_MAP
from .parsing import Parser, ProcedureParser, OpParser
from .compilation import Compiler
from .runtime import Ctx, Interpreter, Session

N_REGISTERS = 16
MEM_SIZE = 64


def spawn_session(
    n_registers,
    mem_size,
    syntax_tokens=None,
    tspec_regexp_map=None
):
    lexer = Lexer(syntax_tokens=syntax_tokens, tspec_regexp_map=tspec_regexp_map)
    parser = Parser(proc_parser=ProcedureParser(), op_parser=OpParser())
    compiler = Compiler()
    ctx = Ctx(n_registers=n_registers, mem_size=mem_size)
    ctx.spawn()
    interpreter = Interpreter(ctx)
    sess = Session(
        lexer=lexer,
        parser=parser,
        compiler=compiler,
        interpreter=interpreter
    )
    return sess


def main(fp, n_registers=None, mem_size=None):
    n_registers = n_registers or N_REGISTERS
    mem_size = mem_size or MEM_SIZE

    sess = spawn_session(
        n_registers=n_registers,
        mem_size=mem_size,
        syntax_tokens=SYNTAX_TOKENS,
        tspec_regexp_map=TSPEC_REGEXP_MAP
    )
    with open(fp, 'r') as src:
        sess.execute(src.read())
