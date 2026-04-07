from enum import Enum


class TokenType(Enum):
    # One char tokens
    COMMA = ','
    DOT = '.'
    COLON = ':'
    QUESTION = '?'
    # Calc
    MINUS = '-'
    PLUS = '+'
    STAR = '*'
    SLASH = '/'
    PERCENT = '%'
    GREATER = '>'
    LESS = '<'
    # Blocks
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    SEMICOLON = ';'

    # Double char tokens
    STAR_STAR = '**'
    PLUS_PLUS = '++'
    MINUS_MINUS = '--'
    EQUAL_EQUAL = '=='
    BANG_EQUAL = '!='
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='

    # Keywords
    NIL = 'nil'
    FUN = 'fun'
    RETURN = 'return'
    PRINT = 'print'
    VAR = 'var'
    # Logical
    TRUE = 'true'
    FALSE = 'false'
    AND = 'and'
    OR = 'or'
    NOT = '!'
    # Flow
    IF = 'if'
    ELSE = 'else'
    # Loops
    WHILE = 'while'
    FOR = 'for'

    # Literals
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    # EOF
    EOF = 'EOF'
