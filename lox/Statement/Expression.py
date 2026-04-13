from Statement import Statement
from Expression import Expression

class Expression(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self) -> str:
        return f"{self.expression}"
