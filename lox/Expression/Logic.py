from Expression import Expression
from Token import Token

class Logic(Expression):
    """
    Examples:
        left and right
        left or right
    """
    
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"