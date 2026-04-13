from Statement import Statement

class Print(Statement):
    def __init__(self, expression: Statement):
        self.expression = expression

    def __str__(self) -> str:
        return f"print {self.expression}"