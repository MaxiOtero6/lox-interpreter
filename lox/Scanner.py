from lox.Token.Token import KeywordsMap, LiteralType, Token
from lox.Token.TokenType import TokenType


class Scanner():
    def __init__(self):
        self.tokens: list[Token] = []
        self.source: str = ""
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        pass

    def scan(self, source: str) -> list[Token]:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.start = self.current
        self._add_token(TokenType.EOF)

        return self.tokens

    def _scan_token(self) -> None:
        c = self._advance()
        
        match c:
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1

            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case ":":
                self._add_token(TokenType.COLON)
            case "?":
                self._add_token(TokenType.QUESTION)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "%":
                self._add_token(TokenType.PERCENT)

            case "/":
                if self._match("/"):
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)

            case "!":
                self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.NOT)
            case ">":
                self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
            case "<":
                self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
            case "+":
                self._add_token(TokenType.PLUS_PLUS if self._match("+") else TokenType.PLUS)
            case "-":
                self._add_token(TokenType.MINUS_MINUS if self._match("-") else TokenType.MINUS)
            case "*":
                self._add_token(TokenType.STAR_STAR if self._match("*") else TokenType.STAR)

            
            case '"':
                self._string()
            
            case _ if c.isdigit():
                self._number()

            case _ if self._is_alpha(c):
                self._identifier()

            case _:
                raise SyntaxError(f"Unexpected character '{c}' at line {self.line}")
            

    def _add_token(
        self,
        token_type: TokenType,
        literal: LiteralType = None,
    ) -> None:
        lexeme = self.source[self.start:self.current]
        token = Token(token_type, lexeme=lexeme, literal=literal)
        self.tokens.append(token)

    def _string(self) -> None:
        while not self._is_at_end() and self._peek() != '"':
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            print(f"[line {self.line}] Error: Unterminated string.")
            return

        self._advance()

        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, literal=value)

    def _number(self) -> None:
        while not self._is_at_end() and self._peek().isdigit():
            self._advance()
        if not self._is_at_end() and self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while not self._is_at_end() and self._peek().isdigit():
                self._advance()
        value = float(self.source[self.start:self.current])
        self._add_token(TokenType.NUMBER, literal=value)

    def _identifier(self) -> None:
        while not self._is_at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        lexeme = self.source[self.start:self.current]
        token_type = KeywordsMap.get(lexeme, TokenType.IDENTIFIER)
        self._add_token(token_type)


    def _is_at_end(self) -> bool:
        if self.current >= len(self.source):
            return True
        return False
        

    def _advance(self) -> str:
        actual = self.source[self.current]
        self.current += 1
        return actual

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]
        

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def _is_alpha(self, c: str) -> bool:
        return c.isalpha() or c == "_"

    def _is_alpha_numeric(self, c: str) -> bool:
        return c.isalnum() or c == "_"
