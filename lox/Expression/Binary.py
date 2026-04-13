from Token import Token

from Expression import Expression


class Binary(Expression):
    """
    Examples:
        left + right
        left - right
        left * right
        left / right
        left % right
    """
    
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
