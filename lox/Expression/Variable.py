from lox.Expression.Expression import Expression
from lox.Token.Token import Token


class Variable(Expression):
    """
    Examples:
        variable
    """

    def __init__(self, name: Token):
        self.name = name

    def __str__(self):
        return str(self.name.lexeme)

    def ast_label(self):
        return "Variable"

    def ast_children(self):
        return [self.name]
