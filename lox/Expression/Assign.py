from Expression import Expression
from Token import Token

class Assign(Expression):
    """
    Examples:
        name = value
    """
    def __init__(self, name: Token, value: Expression):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name.lexeme} = {self.value}"