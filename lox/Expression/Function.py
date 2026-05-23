from typing import List

from lox.Expression.Expression import Expression
from lox.Statement.Statement import Statement
from lox.Token.Token import Token


class Function(Expression):
    def __init__(self, params: List[Token], body: List[Statement]):
        self.params = params
        self.body = body

    def __str__(self) -> str:
        params_joined = ", ".join([p.lexeme for p in self.params])
        statements_joined = "\n".join([str(s) for s in self.body])
        return f"fun ({params_joined}) {{\n{statements_joined}\n}}"

    def ast_label(self):
        params = ", ".join([p.lexeme for p in self.params])
        return f"FunctionLiteral({params})"

    def ast_children(self):
        return list(self.body)
