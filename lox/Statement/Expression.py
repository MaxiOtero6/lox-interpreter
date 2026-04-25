from Statement import Statement
from lox.Expression import Expression as Expr


class Expression(Statement):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self) -> str:
        return f"{self.expression}"
