class Ctx:

    def __init__(self, n_registers, mem_size):
        self.n_registers = n_registers
        self.mem_size = mem_size

        self._reg = None
        self._mem = None
        self._mem_map = None

    def spawn(self):
        self._reg = [0] * self.n_registers
        self._mem = [0] * self.mem_size
        self._mem_map = {}

    def get_reg(self, i):
        if 0 < i >= len(self._reg):
            msg = f'register out of range {i}.'
            raise Exception(msg)

        return self._reg[i]

    def get_mem(self, i):
        if 0 < i >= len(self._mem):
            msg = f'memory out of range {i}.'
            raise Exception(msg)

        return self._mem[i]

    def get_mem_by_name(self, name):
        i = self._mem_map.get(name)

        if i is None:
            msg = f'undefined name {name}.'
            raise Exception(msg)

        return self.get_mem(i)

    def set_reg(self, i, val):
        if 0 < i >= len(self._reg):
            msg = f'register out of range {i}.'
            raise Exception(msg)

        self._reg[i] = val

    def set_mem(self, name):
        pass


class Interpreter:

    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, main_proc):
        main_proc.execute(self.ctx)


class Session:

    def __init__(self, lexer, parser, compiler, interpreter):
        self.lexer = lexer
        self.parser = parser
        self.compiler = compiler
        self.interpreter = interpreter

    def execute(self, src: str):
        tokens = self.lexer(src)
        procs = self.parser(tokens)
        procs = self.compiler.compile_procs(procs)
        main_proc = procs[-1]
        self.interpreter.execute(main_proc)
        print(self.interpreter.ctx._reg)
