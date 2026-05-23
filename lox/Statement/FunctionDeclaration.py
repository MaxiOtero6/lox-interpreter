from lox.Statement.Statement import Statement
from lox.Token.Token import Token


class FunctionDeclaration(Statement):
    def __init__(self, name: Token, params: list[Token], body: list[Statement]):
        self.name = name
        self.params = params
        self.body = body

    def __str__(self) -> str:
        params_joined = ", ".join([param.lexeme for param in self.params])
        statements_joined = "\n".join(
            [str(statement) for statement in self.body]
        )
        return f"fun {self.name.lexeme}({params_joined}) {{\n{statements_joined}\n}}"

    def ast_label(self):
        params = ", ".join([p.lexeme for p in self.params])
        return f"Function {self.name.lexeme}({params})"

    def ast_children(self):
        return list(self.body)
