import pytest
from lox.Scanner import Scanner
from lox.Token.TokenType import TokenType


def test_hello_world():
    tokens = Scanner().scan("2+2")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type


def test_multilne_strings():
    tokens = Scanner().scan('"hello\nworld"')
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.STRING,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type
    assert tokens[0].literal == "hello\nworld"

    tokens = Scanner().scan(
        """
"comentario
con salto de linea"
        """
    )
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.STRING,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type
    assert tokens[0].literal == "comentario\ncon salto de linea"


def test_remove_whitespace():
    expected_tokens_type = [
        TokenType.EOF,
    ]

    tokens = Scanner().scan(" ")
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type

    tokens = Scanner().scan("  ")
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type

    tokens = Scanner().scan("\r")
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type

    tokens = Scanner().scan(
        """

        """
    )
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type


def test_remove_comments():
    expected_tokens_type = [
        TokenType.EOF,
    ]

    tokens = Scanner().scan("// aaaa")
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type


def test_remove_multiline_comments():
    expected_tokens_type = [
        TokenType.EOF,
    ]

    tokens = Scanner().scan(
        """
        /*
        comentario multilinea
        */
        """
    )
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type

    tokens = Scanner().scan(
        """
        /*
        comentario multilinea
        /*
        comentario multilinea anidado
        */
        // otro comentario mas
        */
        """
    )
    tokens_type = [token.type for token in tokens]
    assert tokens_type == expected_tokens_type

    with pytest.raises(Exception) as excinfo:
        Scanner().scan(
            """
            /*
            comentario multilinea
            /*
            comentario multilinea anidado
            */
            // otro comentario mas
            """
        )
    assert "Unterminated multi-line comment" in str(excinfo.value)


def test_single_char_tokens():
    tokens = Scanner().scan("(){}[],-+;*/%:?**")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.MINUS,
        TokenType.PLUS,
        TokenType.SEMICOLON,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.PERCENT,
        TokenType.COLON,
        TokenType.QUESTION,
        TokenType.STAR_STAR,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type


def test_double_char_tokens():
    tokens = Scanner().scan("! != = == < <= > >=")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.NOT,
        TokenType.BANG_EQUAL,
        TokenType.EQUAL,
        TokenType.EQUAL_EQUAL,
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type


def test_string_literal():
    tokens = Scanner().scan('"hello\nworld"')
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.STRING,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type
    assert tokens[0].literal == "hello\nworld"


def test_number_literal():
    tokens = Scanner().scan("123.45")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.NUMBER,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type
    assert tokens[0].literal == 123.45


def test_error_unterminated_string():
    tokens = Scanner().scan('"hello world')
    assert tokens[0].type == TokenType.EOF


def test_identifiers():
    tokens = Scanner().scan("foo bar trueman")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type
    assert tokens[0].lexeme == "foo"
    assert tokens[1].lexeme == "bar"
    assert tokens[2].lexeme == "trueman"


def test_keywords():
    tokens = Scanner().scan(
        "and else false fun for if nil or print return true var while"
    )
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [
        TokenType.AND,
        TokenType.ELSE,
        TokenType.FALSE,
        TokenType.FUN,
        TokenType.FOR,
        TokenType.IF,
        TokenType.NIL,
        TokenType.OR,
        TokenType.PRINT,
        TokenType.RETURN,
        TokenType.TRUE,
        TokenType.VAR,
        TokenType.WHILE,
        TokenType.EOF,
    ]

    assert tokens_type == expected_tokens_type


def test_error_unexpected_character():
    with pytest.raises(Exception) as excinfo:
        Scanner().scan("@")
    assert "Unexpected character" in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        Scanner().scan("`")
    assert "Unexpected character" in str(excinfo.value)


def test_error_invalid_numbers():
    pass


def test_scanner_plus_plus_token():
    tokens = Scanner().scan("++")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [TokenType.PLUS_PLUS, TokenType.EOF]

    assert tokens_type == expected_tokens_type


def test_plus_plus_token_and_plus_token():
    tokens = Scanner().scan("+++")
    tokens_type = [token.type for token in tokens]

    expected_tokens_type = [TokenType.PLUS_PLUS, TokenType.PLUS, TokenType.EOF]

    assert tokens_type == expected_tokens_type
