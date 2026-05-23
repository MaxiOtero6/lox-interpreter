from lox.Statement.Statement import Statement
from lox.Token.Token import Token
from lox.Expression import Expression


class VariableDeclaration(Statement):
    def __init__(self, name: Token, initializer: Expression | None):
        self.name = name
        self.initializer = initializer

    def __str__(self) -> str:
        if self.initializer is None:
            return f"var {self.name.lexeme}"

        return f"var {self.name.lexeme} = {self.initializer}"

    def ast_label(self):
        return f"VarDecl {self.name.lexeme}"

    def ast_children(self):
        return [self.initializer] if self.initializer is not None else []
