from Expression import Expression


class Ternary(Expression):
    """
    Examples:
        condition ? true_expr : false_expr
    """
    def __init__(self, condition: Expression, true_expr: Expression, false_expr: Expression):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __str__(self):
        return f"({self.condition} ? {self.true_expr} : {self.false_expr})"
