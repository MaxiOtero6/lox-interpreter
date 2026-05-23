from lox.Expression.Expression import Expression
from lox.Token.Token import LiteralType
import lox.Printer as Printer


class Literal(Expression):
    """
    Examples:
        123
        "hello"
        true
        false
        nil
    """

    def __init__(self, value: LiteralType):
        self.value = value

    def __str__(self):
        return Printer.stringify(self.value)

    def ast_label(self):
        return "Literal"

    def ast_children(self):
        return [self.value]
