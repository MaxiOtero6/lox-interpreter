from Statement import Statement
from lox.Expression import Expression


class Print(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self) -> str:
        return f"print {self.expression}"
