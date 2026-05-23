from lox.Statement.Statement import Statement
from lox.Expression import Expression as Expr


class Expression(Statement):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self) -> str:
        return f"{self.expression}"

    def ast_label(self):
        return "ExprStmt"

    def ast_children(self):
        return [self.expression]
