from Statement import Statement
from Expression import Expression

class Return(Statement):
    def __init__(self, value: Expression | None):
        self.value = value

    def __str__(self) -> str:
        return f"return {self.value or 'nil'}"