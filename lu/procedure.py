class Procedure:

    def __init__(self):
        self.name = None
        self.tokens = []
        self.args = {}
        self.body = []
        self.ops = []

    def __repr__(self):
        return f'Procedure(name={self.name})'
