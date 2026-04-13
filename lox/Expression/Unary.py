from Expression import Expression
from Token import Token


class Unary(Expression):
    """
    Examples:
        -right
        !right
    """
    
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator}{self.right})"
