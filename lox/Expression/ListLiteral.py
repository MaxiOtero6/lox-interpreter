from lox.Expression.Expression import Expression


class ListLiteral(Expression):
    """
    Examples:
        []
        [1, 2, 3]
    """

    def __init__(self, elements: list[Expression]):
        self.elements = elements

    def __str__(self):
        return f"[{', '.join(map(str, self.elements))}]"

    def ast_label(self):
        return "ListLiteral"

    def ast_children(self):
        return list(self.elements)
