import pytest
from lox.Expression import (
    Binary,
    Group,
    IndexGet,
    IndexSet,
    Literal,
    ListLiteral,
    Prefix,
    Unary,
    Assign,
    Postfix,
    Ternary,
)
from lox.Scanner import Scanner
from lox.Parser import Parser
from lox.Token.TokenType import TokenType
from lox.Statement import (
    Expression,
    Print,
    Block,
    VariableDeclaration,
    FunctionDeclaration,
    Return,
    If,
    While,
)
from lox.Expression import Variable


def test_hello_world():
    tokens = Scanner().scan("2+2")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Binary)
    assert isinstance(expr.left, Literal)
    assert isinstance(expr.right, Literal)
    assert expr.left.value == 2.0
    assert expr.operator.type == TokenType.PLUS
    assert expr.right.value == 2.0


def test_literals():
    tokens = Scanner().scan('"hello"')
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Literal)
    assert expr.value == "hello"

    tokens = Scanner().scan("123")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Literal)
    assert expr.value == 123.0

    tokens = Scanner().scan("true")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Literal)
    assert expr.value is True

    tokens = Scanner().scan("false")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Literal)
    assert expr.value is False

    tokens = Scanner().scan("nil")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Literal)
    assert expr.value is None


def test_list_literals():
    tokens = Scanner().scan("[]")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, ListLiteral)
    assert expr.elements == []

    tokens = Scanner().scan("[1, 2 + 3, \"hello\"]")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, ListLiteral)
    assert len(expr.elements) == 3
    assert isinstance(expr.elements[0], Literal)
    assert expr.elements[0].value == 1.0
    assert isinstance(expr.elements[1], Binary)
    assert isinstance(expr.elements[2], Literal)
    assert expr.elements[2].value == "hello"

    tokens = Scanner().scan("[1, 2")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens)._make_expression()
    assert "TokenType.RIGHT_BRACKET" in str(excinfo.value)


def test_index_get():
    tokens = Scanner().scan("xs[0]")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, IndexGet)
    assert isinstance(expr.collection, Variable)
    assert expr.collection.name.lexeme == "xs"
    assert isinstance(expr.index, Literal)
    assert expr.index.value == 0.0

    tokens = Scanner().scan("[1, 2][0]")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, IndexGet)
    assert isinstance(expr.collection, ListLiteral)
    assert isinstance(expr.index, Literal)
    assert expr.index.value == 0.0

    tokens = Scanner().scan("matrix[0][1]")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, IndexGet)
    assert isinstance(expr.collection, IndexGet)
    assert isinstance(expr.index, Literal)
    assert expr.index.value == 1.0

    tokens = Scanner().scan("xs[0")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens)._make_expression()
    assert "TokenType.RIGHT_BRACKET" in str(excinfo.value)


def test_index_set():
    tokens = Scanner().scan("xs[0] = 99")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, IndexSet)
    assert isinstance(expr.collection, Variable)
    assert expr.collection.name.lexeme == "xs"
    assert isinstance(expr.index, Literal)
    assert expr.index.value == 0.0
    assert isinstance(expr.value, Literal)
    assert expr.value.value == 99.0

    tokens = Scanner().scan("matrix[0][1] = 7")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, IndexSet)
    assert isinstance(expr.collection, IndexGet)
    assert isinstance(expr.index, Literal)
    assert expr.index.value == 1.0
    assert isinstance(expr.value, Literal)
    assert expr.value.value == 7.0

    tokens = Scanner().scan("(xs + 1) = 99")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens)._make_expression()
    assert "Expected assignment target" in str(excinfo.value)


def test_groupings():
    tokens = Scanner().scan("(2 + 2)")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Group)
    assert isinstance(expr.expression, Binary)
    assert isinstance(expr.expression.left, Literal)
    assert expr.expression.left.value == 2.0
    assert expr.expression.operator.type == TokenType.PLUS
    assert isinstance(expr.expression.right, Literal)
    assert expr.expression.right.value == 2.0


def test_unary():
    tokens = Scanner().scan("-123")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Unary)
    assert expr.operator.type == TokenType.MINUS
    assert isinstance(expr.right, Literal)
    assert expr.right.value == 123.0


def test_error_parens():
    tokens = Scanner().scan("(2 + 2")
    parser = Parser(tokens)
    with pytest.raises(Exception) as excinfo:
        parser._make_expression()
    assert "TokenType.RIGHT_PAREN" in str(excinfo.value)


def test_error_incomplete():
    tokens = Scanner().scan("1 + ")
    parser = Parser(tokens)
    with pytest.raises(Exception) as excinfo:
        parser._make_expression()
    assert "Expected expression" in str(excinfo.value)


def test_associativity():
    # ## This resolves to: (5 - 3) - 1
    tokens = Scanner().scan("5 - 3 - 1")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.MINUS

    left = expr.left
    right = expr.right

    assert isinstance(left, Binary)
    assert left.operator.type == TokenType.MINUS
    assert isinstance(left.left, Literal)
    assert left.left.value == 5.0
    assert isinstance(left.right, Literal)
    assert left.right.value == 3.0

    assert isinstance(right, Literal)
    assert right.value == 1.0


def test_precedence():
    tokens = Scanner().scan("1 + 2 * 3 - 4")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.MINUS

    left = expr.left
    assert isinstance(left, Binary)
    assert left.operator.type == TokenType.PLUS
    assert isinstance(left.left, Literal)
    assert left.left.value == 1.0

    left_right = left.right
    assert isinstance(left_right, Binary)
    assert left_right.operator.type == TokenType.STAR
    assert isinstance(left_right.left, Literal)
    assert left_right.left.value == 2.0
    assert isinstance(left_right.right, Literal)
    assert left_right.right.value == 3.0

    right = expr.right
    assert isinstance(right, Literal)
    assert right.value == 4.0


def test_precedence_unary():
    tokens = Scanner().scan("-1+2")
    expr = Parser(tokens)._make_expression()

    # ## Esto tiene que dar (-1) + 2, no -(1+2)
    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.PLUS
    assert isinstance(expr.left, Unary)
    assert expr.left.operator.type == TokenType.MINUS
    assert isinstance(expr.left.right, Literal)
    assert expr.left.right.value == 1.0
    assert isinstance(expr.right, Literal)
    assert expr.right.value == 2.0


def test_big():
    tokens = Scanner().scan("1 - (2 * 3) < 4 == false")
    expr = Parser(tokens)._make_expression()

    # Top-level == false
    assert isinstance(expr, Binary)
    assert expr.operator.type == TokenType.EQUAL_EQUAL

    left = expr.left
    right = expr.right

    # ## Right side is literal false
    assert isinstance(right, Literal)
    assert right.value is False

    # Left side is (1 - (2 * 3)) < 4
    assert isinstance(left, Binary)
    assert left.operator.type == TokenType.LESS

    # Right of < is 4
    assert isinstance(left.right, Literal)
    assert left.right.value == 4.0

    # Left of < is (1 - (2 * 3))
    assert isinstance(left.left, Binary)
    assert left.left.operator.type == TokenType.MINUS

    minus_left = left.left.left
    minus_right = left.left.right

    assert isinstance(minus_left, Literal)
    assert minus_left.value == 1.0

    # minus_right is a grouping with inner multiplication
    assert isinstance(minus_right, Group)
    inner = minus_right.expression
    assert isinstance(inner, Binary)
    assert inner.operator.type == TokenType.STAR
    assert isinstance(inner.left, Literal)
    assert inner.left.value == 2.0
    assert isinstance(inner.right, Literal)
    assert inner.right.value == 3.0


def test_expression_stmt():
    tokens = Scanner().scan("123; 456;")
    stmts = Parser(tokens).parse()
    assert len(stmts) == 2
    assert isinstance(stmts[0], Expression)
    assert isinstance(stmts[0].expression, Literal)
    assert stmts[0].expression.value == 123.0
    assert isinstance(stmts[1], Expression)
    assert isinstance(stmts[1].expression, Literal)
    assert stmts[1].expression.value == 456.0


def test_print_stmt():
    tokens = Scanner().scan('print "hola";')
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    stmt = stmts[0]
    assert isinstance(stmt, Print)
    assert isinstance(stmt.expression, Literal)
    assert stmt.expression.value == "hola"


def test_block_stmt():
    tokens = Scanner().scan("{ 1; 2; }")
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    stmt = stmts[0]
    assert isinstance(stmt, Block)
    assert len(stmt.statements) == 2
    assert isinstance(stmt.statements[0], Expression)
    assert isinstance(stmt.statements[1], Expression)


def test_var_decl():
    tokens = Scanner().scan("var x = 5;")
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    stmt = stmts[0]
    assert isinstance(stmt, VariableDeclaration)
    assert stmt.name.lexeme == "x"
    assert isinstance(stmt.initializer, Literal)
    assert stmt.initializer.value == 5.0


def test_assignment():
    tokens = Scanner().scan("x = 5;")
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    stmt = stmts[0]
    assert isinstance(stmt, Expression)
    assert isinstance(stmt.expression, Assign)
    assert stmt.expression.name.lexeme == "x"
    assert isinstance(stmt.expression.value, Literal)
    assert stmt.expression.value.value == 5.0

    tokens = Scanner().scan("(x) = 5;")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens).parse()
    assert "Expected assignment target" in str(excinfo.value)

    tokens = Scanner().scan("a + b = 5;")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens).parse()
    assert "Expected assignment target" in str(excinfo.value)


def test_function_decl_and_return():
    src = "fun add(a, b) { return a; }"
    tokens = Scanner().scan(src)
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    fn = stmts[0]
    assert isinstance(fn, FunctionDeclaration)
    assert fn.name.lexeme == "add"
    assert [p.lexeme for p in fn.params] == ["a", "b"]
    assert len(fn.body) == 1
    ret = fn.body[0]
    assert isinstance(ret, Return)
    assert isinstance(ret.value, Variable)
    assert ret.value.name.lexeme == "a"


def test_return_stmt():
    tokens = Scanner().scan("return 3;")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], Return)
    assert isinstance(stmts[0].value, Literal)
    assert stmts[0].value.value == 3.0

    tokens = Scanner().scan("return;")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], Return)
    assert stmts[0].value is None


def test_block_stmts():
    tokens = Scanner().scan("{ print a; }")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], Block)
    assert len(stmts[0].statements) == 1
    assert isinstance(stmts[0].statements[0], Print)

    tokens = Scanner().scan("{ print a; ")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens).parse()
    assert "TokenType.RIGHT_BRACE" in str(excinfo.value)


def test_control_flow():
    tokens = Scanner().scan("if (true) 1; else 2;")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], If)
    ifs = stmts[0]
    assert isinstance(ifs.condition, Literal)
    assert ifs.condition.value is True
    assert isinstance(ifs.then_branch, Expression)
    assert isinstance(ifs.else_branch, Expression)

    tokens = Scanner().scan("while (false) 3;")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], While)
    w = stmts[0]
    assert isinstance(w.condition, Literal)
    assert w.condition.value is False
    assert isinstance(w.body, Expression)


def test_for():
    tokens = Scanner().scan("for (var i = 0 ; i < 3 ; i = i + 1) { print 0; }")
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    stmt = stmts[0]

    assert isinstance(stmt, Block)
    assert isinstance(stmt.statements[0], VariableDeclaration)
    assert stmt.statements[0].name.lexeme == "i"
    assert isinstance(stmt.statements[1], While)
    ws = stmt.statements[1]
    assert isinstance(ws.condition, Binary)
    assert ws.condition.operator.type == TokenType.LESS

    assert isinstance(ws.body, Block)
    assert isinstance(ws.body.statements[0], Block)
    assert isinstance(ws.body.statements[0].statements[0], Print)
    assert isinstance(ws.body.statements[1], Expression)
    assert isinstance(ws.body.statements[1].expression, Assign)

    tokens = Scanner().scan("for ( ; i < 3 ; i = i + 1) { print 0; }")
    stmts = Parser(tokens).parse()
    assert len(stmts) == 1
    assert isinstance(stmts[0], While)

    tokens = Scanner().scan("for (var i = 0 ;  ; i = i + 1) { print 0; }")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], Block)
    stmt = stmts[0]
    assert isinstance(stmt.statements[0], VariableDeclaration)
    assert isinstance(stmt.statements[1], While)
    assert isinstance(stmt.statements[1].condition, Literal)
    assert stmt.statements[1].condition.value is True

    tokens = Scanner().scan("for (var i = 0 ; i < 3 ; ) { print 0; }")
    stmts = Parser(tokens).parse()
    assert isinstance(stmts[0], Block)
    stmt = stmts[0]
    assert isinstance(stmt.statements[1], While)
    inner_body = stmt.statements[1].body
    assert isinstance(inner_body, Block)
    assert len(inner_body.statements) == 1
    assert isinstance(inner_body.statements[0], Print)


def test_postfix_inc():
    tokens = Scanner().scan("x++")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Postfix)
    assert expr.operator.type == TokenType.PLUS_PLUS
    assert isinstance(expr.left, Variable)
    assert expr.left.name.lexeme == "x"

    tokens = Scanner().scan("-x++")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Unary)
    assert isinstance(expr.right, Postfix)

    tokens = Scanner().scan("x++ + 1")
    expr = Parser(tokens)._make_expression()
    assert isinstance(expr, Binary)
    assert isinstance(expr.left, Postfix)
    assert isinstance(expr.right, Literal)

    tokens = Scanner().scan("1++")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens).parse()
    assert "Expected variable before postfix operator" in str(excinfo.value)


def test_prefix_inc():
    tokens = Scanner().scan("++x")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Prefix)
    assert isinstance(expr.right, Variable)
    assert expr.right.name.lexeme == "x"


def test_ternary():
    tokens = Scanner().scan("true ? 1 : 2")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Ternary)
    assert isinstance(expr.condition, Literal)
    assert expr.condition.value == True
    assert isinstance(expr.true_expr, Literal)
    assert expr.true_expr.value == 1.0
    assert isinstance(expr.false_expr, Literal)
    assert expr.false_expr.value == 2.0

    tokens = Scanner().scan("true ? true ? 1 : 2 : true ? 1 : 2")
    expr = Parser(tokens)._make_expression()

    assert isinstance(expr, Ternary)
    assert isinstance(expr.true_expr, Ternary)
    assert isinstance(expr.false_expr, Ternary)

    tokens = Scanner().scan("true ? 1")
    with pytest.raises(Exception) as excinfo:
        Parser(tokens).parse()
    assert "TokenType.COLON" in str(excinfo.value)


def test_power():
    pass
