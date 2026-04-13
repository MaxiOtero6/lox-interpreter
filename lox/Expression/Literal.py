from Expression import Expression
from Token import LiteralType


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
        return str(self.value)
