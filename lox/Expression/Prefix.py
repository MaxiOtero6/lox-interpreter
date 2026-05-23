from lox.Expression.Expression import Expression
from lox.Token.Token import Token


class Prefix(Expression):
    """
    Examples:
        ++left
        --left
    """

    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.operator}{self.right})"
