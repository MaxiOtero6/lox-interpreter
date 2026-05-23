from lox.Statement.Statement import Statement
from lox.Expression import Expression


class Return(Statement):
    def __init__(self, value: Expression | None):
        self.value = value

    def __str__(self) -> str:
        return f"return {self.value or 'nil'}"

    def ast_label(self):
        return "Return"

    def ast_children(self):
        return [self.value] if self.value is not None else []
