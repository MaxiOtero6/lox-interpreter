from lox.Expression.Expression import Expression


class Call(Expression):
    """
    Examples:
        callee(arguments)
    """

    def __init__(self, callee: Expression, arguments: list[Expression]):
        self.callee = callee
        self.arguments = arguments

    def __str__(self):
        return f"{self.callee}({', '.join(map(str, self.arguments))})"

    def ast_label(self):
        return "Call"

    def ast_children(self):
        children = [self.callee]
        children.extend(self.arguments)
        return children
