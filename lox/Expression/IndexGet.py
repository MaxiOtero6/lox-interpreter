from lox.Expression.Expression import Expression


class IndexGet(Expression):
    """
    Examples:
        list[index]
    """

    def __init__(self, collection: Expression, index: Expression):
        self.collection = collection
        self.index = index

    def __str__(self):
        return f"{self.collection}[{self.index}]"

    def ast_label(self):
        return "IndexGet"

    def ast_children(self):
        return [self.collection, self.index]
