from lox.Token.TokenType import TokenType


LiteralType = str | float | bool | None

KeywordsMap = {
    'and': TokenType.AND,
    'else': TokenType.ELSE,
    'false': TokenType.FALSE,
    'for': TokenType.FOR,
    'fun': TokenType.FUN,
    'if': TokenType.IF,
    'nil': TokenType.NIL,
    'or': TokenType.OR,
    'print': TokenType.PRINT,
    'return': TokenType.RETURN,
    'true': TokenType.TRUE,
    'var': TokenType.VAR,
    'while': TokenType.WHILE
}


class Token():
    def __init__(self, type: TokenType, lexeme: str, literal: LiteralType, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
