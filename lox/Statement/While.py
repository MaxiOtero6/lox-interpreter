from lox.Statement.Statement import Statement
from lox.Expression import Expression


class While(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return f"while {self.condition} {self.body}"

    def ast_label(self):
        return "While"

    def ast_children(self):
        return [self.condition, self.body]
