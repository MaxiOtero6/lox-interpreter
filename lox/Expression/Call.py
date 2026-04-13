from Expression import Expression


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