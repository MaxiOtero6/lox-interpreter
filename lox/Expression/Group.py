from Expression import Expression


class Group(Expression):
    """
    Examples:
        (expression)
    """
    
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"({self.expression})"
