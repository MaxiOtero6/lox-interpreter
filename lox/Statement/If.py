from Statement import Statement
from Expression import Expression

class If(Statement):
    def __init__(self, condition: Expression, then_branch: Statement, else_branch: Statement | None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __str__(self) -> str:
        return f"if {self.condition} then {self.then_branch}" + (f" else {self.else_branch}" if self.else_branch else "")