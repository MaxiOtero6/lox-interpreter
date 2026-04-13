from Expression import Expression
from Token import Token

class Postfix(Expression):
    """
    Examples:
        left++
        left--
    """

    def __init__(self, operator: Token, left: Expression):
        self.operator = operator
        self.left = left

    def __str__(self):
        return f"({self.left}{self.operator})"