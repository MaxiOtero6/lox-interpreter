import pytest
from lox.Interpreter import Interpreter
from lox.Scanner import Scanner
from lox.Parser import Parser


def test_hello_world():
    tokens = Scanner().scan("2+2")
    expr = Parser(tokens)._make_expression()
    value = Interpreter().evaluate(expr)
    assert value == 4.0


def test_calc():
    tokens = Scanner().scan("1 + 2 * 3 - 4")
    expr = Parser(tokens)._make_expression()
    value = Interpreter().evaluate(expr)
    assert value == 3

    tokens = Scanner().scan("6 / 3 - 1")
    expr = Parser(tokens)._make_expression()
    value = Interpreter().evaluate(expr)
    assert value == 1


def test_various_expressions():
    tests = [
        ('"aaa"', "aaa"),
        ("123", 123.0),
        ('"a" + "b"', "ab"),
        ("2 + 2", 4.0),
        ("4 - 2", 2.0),
        ("5 * 5", 25.0),
        ("3 > 2", True),
        ("3 >= 3", True),
        ("3 == 3", True),
        ('"aa" == "aa"', True),
        ("3 > 4", False),
        ("3 >= 4", False),
        ("3 == 4", False),
        ('"ab" == "aa"', False),
        ("42", 42),
        ("-42", -42),
        ("-( - - 1)", -1),
        ("((((0))))", 0),
        ("0 + 1", 1),
        ("4 - 2", 2),
        ("1.5 * 2", 3),
        ("8 / 2", 4),
        ("1 + 2 * 3 - 4 + 2", 5),
        ("3 * (3 - 1)", 6),
        ("((1 + 2) * (3 + 4)) / 3", 7),
        ("1 * 0", 0),
    ]

    for expr, expected in tests:
        tokens = Scanner().scan(expr)
        expr = Parser(tokens)._make_expression()
        value = Interpreter().evaluate(expr)
        assert value == expected


def test_errors():
    tokens = Scanner().scan('"aaa" + 5')
    expr = Parser(tokens)._make_expression()
    with pytest.raises(RuntimeError) as excinfo:
        Interpreter().evaluate(expr)

    assert "Operands of + must be either numbers or strings" in str(excinfo.value)

    tokens = Scanner().scan('-"aaa"')
    expr = Parser(tokens)._make_expression()
    with pytest.raises(RuntimeError) as excinfo:
        Interpreter().evaluate(expr)

    assert "Operand must be a number" in str(excinfo.value)

    tokens = Scanner().scan('-"aaa"')
    expr = Parser(tokens)._make_expression()
    with pytest.raises(RuntimeError) as excinfo:
        Interpreter().evaluate(expr)

    tokens = Scanner().scan('"aaa" - "bbb"')
    expr = Parser(tokens)._make_expression()
    with pytest.raises(RuntimeError) as excinfo:
        Interpreter().evaluate(expr)

    assert "Binary operator TokenType.MINUS not implemented" in str(excinfo.value) or "Operands of - must be numbers" in str(excinfo.value)

    tokens = Scanner().scan("5 / 0")
    expr = Parser(tokens)._make_expression()
    with pytest.raises(ZeroDivisionError) as excinfo:
        Interpreter().evaluate(expr)

    


def test_logic():
    tests = [
        ("true and true", True),
        ("true and false", False),
        ("false and true", False),
        ("false and false", False),
        ("true or true", True),
        ("true or false", True),
        ("false or true", True),
        ("false or false", False),
    ]

    for src, expected in tests:
        tokens = Scanner().scan(src)
        expr = Parser(tokens)._make_expression()
        value = Interpreter().evaluate(expr)
        assert value == expected


def test_ternary():
    tests = [
        ("true ? 1 : 2", 1),
        ("false ? 1 : 2", 2),
        ("true ? true ? 1 : 2 : 3", 1),
        ("true ? false ? 1 : 2 : 3", 2),
        ("false ? true ? 1 : 2 : 3", 3),
        ("false ? 1 : true ? 2 : 3", 2),
        ("false ? 1 : false ? 2 : 3", 3),
    ]

    for src, expected in tests:
        tokens = Scanner().scan(src)
        expr = Parser(tokens)._make_expression()
        value = Interpreter().evaluate(expr)
        assert value == expected
