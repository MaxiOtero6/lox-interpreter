from lox.Statement.Statement import Statement
from lox.Expression import Expression


class Print(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self) -> str:
        return f"print {self.expression}"

    def ast_label(self):
        return "Print"

    def ast_children(self):
        return [self.expression]
