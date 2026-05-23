from lox.Expression.Expression import Expression


class Group(Expression):
    """
    Examples:
        (expression)
    """

    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"({self.expression})"

    def ast_label(self):
        return "Group"

    def ast_children(self):
        return [self.expression]
