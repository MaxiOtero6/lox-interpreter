from lox.Statement.Statement import Statement


class Block(Statement):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def __str__(self) -> str:
        return f"{{\n{''.join([str(statement) for statement in self.statements])}\n}}"

    def ast_label(self):
        return "Block"

    def ast_children(self):
        return list(self.statements)
