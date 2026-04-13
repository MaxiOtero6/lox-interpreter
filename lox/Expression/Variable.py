from Expression import Expression
from Token import Token


class Variable(Expression):
    """
    Examples:
        variable
    """

    def __init__(self, name: Token):
        self.name = name

    def __str__(self):
        return str(self.name.lexeme)
