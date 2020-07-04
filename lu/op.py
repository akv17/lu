class Op:

    def __init__(self):
        self.name = None
        self.tokens = []
        self.args = []

    def __repr__(self):
        return f'Op(name={self.name})'
