from lox.Expression.Expression import Expression


class IndexSet(Expression):
    """
    Examples:
        list[index] = value
    """

    def __init__(self, collection: Expression, index: Expression, value: Expression):
        self.collection = collection
        self.index = index
        self.value = value

    def __str__(self):
        return f"{self.collection}[{self.index}] = {self.value}"

    def ast_label(self):
        return "IndexSet"

    def ast_children(self):
        return [self.collection, self.index, self.value]
