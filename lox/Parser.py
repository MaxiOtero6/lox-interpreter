import lox.Statement as Statement
import lox.Expression as Expression
from lox.Token.Token import Token
from lox.Token.TokenType import TokenType


class Parser():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pointer = 0

    def parse(self):
        statements: list[Statement.Statement] = []

        while not self._look_next().type == TokenType.EOF:
            statements.append(self._make_statement())

        return statements

    def _look_next(self) -> Token:
        """
        Returns the next token without consuming it.
        """
        
        return self.tokens[self.pointer + 1]

    def _next(self) -> Token:
        """
        Returns the next token and consumes it.
        """
        
        if not self._look_next().type == TokenType.EOF:
            self.pointer += 1

        return self.tokens[self.pointer]

    def _prev(self) -> Token:
        """
        Returns the previous token.
        """
        
        return self.tokens[self.pointer - 1]

    def _match(self, types: set[TokenType]) -> bool:
        """
        Matches the next token if it is of the specified type.
        If the next token is of the specified type, it is consumed and True is returned.
        Otherwise, False is returned and the token is not consumed.
        """
        
        if self._look_next().type in types:
            self._next()
            return True

        return False

    # ------------------- STATEMENT PARSING ------------------ #

    def _make_statement(self) -> Statement.Statement:
        """
            Statement factory
        """
        
        if self._match({TokenType.VAR}):
            return self._make_var_statement()

        if self._match({TokenType.FUN}):
            return self._make_fun_statement()

        if self._match({TokenType.RETURN}):
            return self._make_return_statement()

        if self._match({TokenType.IF}):
            return self._make_if_statement()

        if self._match({TokenType.WHILE}):
            return self._make_while_statement()

        if self._match({TokenType.FOR}):
            return self._make_for_statement()

        if self._match({TokenType.LEFT_BRACE}):
            return self._make_block_statement()

        if self._match({TokenType.PRINT}):
            return self._make_print_statement()

        return self._make_expression_statement()

    def _make_print_statement(self) -> Statement.Statement:
        """
            Parses a print statement.
                print <expression>;
        """
        
        expression = self._make_expression()

        if not self._match({TokenType.SEMICOLON}):
            raise SyntaxError(
                f"Expected '{TokenType.SEMICOLON}' after value instead got '{self._look_next().type}'")

        return Statement.Print(expression)

    def _make_var_statement(self) -> Statement.Statement:
        """
            Parses a variable declaration statement.
                var <name> = <expression>;
        """
        
        if not self._match({TokenType.IDENTIFIER}):
            raise SyntaxError(
                f"Expected variable name after 'var' instead got '{self._look_next().type}'")

        name = self._prev()

        value = self._make_expression() if self._match(
            {TokenType.EQUAL}) else None

        if not self._match({TokenType.SEMICOLON}):
            raise SyntaxError(
                f"Expected '{TokenType.SEMICOLON}' after variable declaration instead got '{self._look_next().type}'")

        return Statement.VariableDeclaration(name, value)

    def _make_fun_statement(self) -> Statement.Statement:
        """
            Parses a function declaration statement.
                fun <name>(<params>) { <body> }
        """
        
        if not self._match({TokenType.IDENTIFIER}):
            raise SyntaxError(
                f"Expected function name after 'fun' instead got '{self._look_next().type}'")

        name = self._prev()
        params: list[Token] = []

        if not self._match({TokenType.LEFT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.LEFT_PAREN}' after function name instead got '{self._look_next().type}'")

        while not self._look_next().type in {TokenType.EOF, TokenType.RIGHT_PAREN}:
            if not self._match({TokenType.IDENTIFIER}):
                raise SyntaxError(
                    f"Expected parameter name instead got '{self._look_next().type}'")

            params.append(self._prev())

            if self._look_next().type == TokenType.COMMA:
                self._next()

        if not self._match({TokenType.RIGHT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.RIGHT_PAREN}' after parameters instead got '{self._look_next().type}'")

        if not self._match({TokenType.LEFT_BRACE}):
            raise SyntaxError(
                f"Expected '{TokenType.LEFT_BRACE}' before function body instead got '{self._look_next().type}'")

        body = self._get_block()

        return Statement.FunctionDeclaration(name, params, body)

    def _make_return_statement(self) -> Statement.Statement:
        """
            Parses a return statement.
                return <expression>;
        """
        
        value = self._make_expression() if not self._look_next(
        ).type == TokenType.SEMICOLON else None

        if not self._match({TokenType.SEMICOLON}):
            raise SyntaxError(
                f"Expected '{TokenType.SEMICOLON}' after return value instead got '{self._look_next().type}'")

        return Statement.Return(value)

    def _make_if_statement(self) -> Statement.Statement:
        """
            Parses an if statement.
                if (<condition>) <then_branch> else <else_branch>
        """
        
        if not self._match({TokenType.LEFT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.LEFT_PAREN}' after 'if' instead got '{self._look_next().type}'")

        condition = self._make_expression()

        if not self._match({TokenType.RIGHT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.RIGHT_PAREN}' after condition instead got '{self._look_next().type}'")

        then_branch = self._make_statement()
        else_branch = self._make_statement() if self._match(
            {TokenType.ELSE}) else None

        return Statement.If(condition, then_branch, else_branch)

    def _make_while_statement(self) -> Statement.Statement:
        """
            Parses a while statement.
                while (<condition>) <body>
        """
        
        if not self._match({TokenType.LEFT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.LEFT_PAREN}' after 'while' instead got '{self._look_next().type}'")

        condition = self._make_expression()

        if not self._match({TokenType.RIGHT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.RIGHT_PAREN}' after condition instead got '{self._look_next().type}'")

        body = self._make_statement()

        return Statement.While(condition, body)

    def _make_for_statement(self) -> Statement.Statement:
        """
            Parses a for statement.
                for (<initializer>; <condition>; <increment>) <body>
            Internally, a for statement is desugared into a while statement with the following structure:
                {
                    <initializer>;
                    while (<condition>) {
                        <body>;
                        <increment>;
                    }
                }        
        """

        if not self._match({TokenType.LEFT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.LEFT_PAREN}' after 'for' instead got '{self._look_next().type}'")

        initializer: Statement.Statement | None = None
        if self._match({TokenType.SEMICOLON}):
            initializer = None
        elif self._match({TokenType.VAR}):
            initializer = self._make_var_statement()
        else:
            initializer = self._make_expression_statement()

        condition = self._make_expression() if not self._look_next(
        ).type == TokenType.SEMICOLON else None

        if not self._match({TokenType.SEMICOLON}):
            raise SyntaxError(
                f"Expected '{TokenType.SEMICOLON}' after loop condition instead got '{self._look_next().type}'")

        increment = self._make_expression() if not self._look_next(
        ).type == TokenType.RIGHT_PAREN else None

        if not self._match({TokenType.RIGHT_PAREN}):
            raise SyntaxError(
                f"Expected '{TokenType.RIGHT_PAREN}' after for clauses instead got '{self._look_next().type}'")

        body = self._make_statement()

        if increment is not None:
            body = Statement.Block([body, Statement.Expression(increment)])

        if condition is None:
            condition = Expression.Literal(True)

        body = Statement.While(condition, body)

        if initializer is not None:
            body = Statement.Block([initializer, body])

        return body

    def _get_block(self) -> list[Statement.Statement]:
        """
            Parses a block statement into a list of statements.
                { <statements> }
        """
        
        statements: list[Statement.Statement] = []
        while not self._look_next().type in {TokenType.EOF, TokenType.RIGHT_BRACE}:
            statements.append(self._make_statement())

        if not self._match({TokenType.RIGHT_BRACE}):
            raise SyntaxError(
                f"Expected '{TokenType.RIGHT_BRACE}' after block instead got '{self._look_next().type}'")

        return statements

    def _make_block_statement(self) -> Statement.Statement:   
        """
            Parses a block statement.
                { <statements> }
        """
             
        return Statement.Block(self._get_block())

    def _make_expression_statement(self) -> Statement.Statement:
        """
            Parses an expression statement.
                <expression>;
        """
        expression = self._make_expression()

        if not self._match({TokenType.SEMICOLON}):
            raise SyntaxError(
                f"Expected '{TokenType.SEMICOLON}' after expression instead got '{self._look_next().type}'")

        return Statement.Expression(expression)

    # ------------------- EXPRESSION PARSING ------------------ #

    def _make_expression(self) -> Expression.Expression:
        """
            Expression factory. It resolves the AST nodes precedence and associativity 
            by calling the corresponding parsing method for each precedence level 
            to achieve the correct order of operations in the resulting AST.
            
            The precedence levels are as follows (from lowest to highest):
                - Assignment
                - Ternary
                - Logical OR
                - Logical AND
                - Equality
                - Comparison
                - Term
                - Factor
                - Unary
                - Postfix
                - Call
                - Primary
        """
        
        return self._make_assignment_expression()

    def _make_assignment_expression(self) -> Expression.Expression:
        """
            Parses an assignment expression.
                <variable> = <expression>
        """
        
        expression = self._make_ternary_expression()

        if not self._match({TokenType.EQUAL}):
            return expression

        if not isinstance(expression, Expression.Variable):
            raise SyntaxError(
                f"Expected variable on left side of assignment instead got '{expression}'")

        value = self._make_expression()
        return Expression.Assign(expression.name, value)

    def _make_ternary_expression(self) -> Expression.Expression:
        """
            Parses a ternary expression.
                <condition> ? <true_branch> : <false_branch>
        """
        
        expression = self._make_assignment_expression()

        if not self._match({TokenType.QUESTION}):
            return expression

        true_branch = self._make_expression()
        if not self._match({TokenType.COLON}):
            raise SyntaxError(
                f"Expected '{TokenType.COLON}' after true branch instead got '{self._look_next().type}'")

        false_branch = self._make_expression()
        expression = Expression.Ternary(expression, true_branch, false_branch)
        return expression

    def _make_logical_or_expression(self) -> Expression.Expression:
        """
            Parses a logical OR expression.
                <left> or <right>
        """
        
        expression = self._make_logical_and_expression()

        while not self._look_next().type == TokenType.EOF and self._match({TokenType.OR}):
            operator = self._prev()
            right = self._make_logical_and_expression()
            expression = Expression.Logic(expression, operator, right)

        return expression

    def _make_logical_and_expression(self) -> Expression.Expression:
        """
            Parses a logical AND expression.
                <left> and <right>
        """
        
        expression = self._make_equality_expression()

        while not self._look_next().type == TokenType.EOF and self._match({TokenType.AND}):
            operator = self._prev()
            right = self._make_equality_expression()
            expression = Expression.Logic(expression, operator, right)

        return expression

    def _make_equality_expression(self) -> Expression.Expression:
        """
            Parses an equality expression.
                <left> == <right>
                <left> != <right>
        """
        
        expression = self._make_comparison_expression()

        while not self._look_next().type == TokenType.EOF and self._match({TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL}):
            operator = self._prev()
            right = self._make_comparison_expression()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _make_comparison_expression(self) -> Expression.Expression:
        """
            Parses a comparison expression.
                <left> > <right>
                <left> >= <right>
                <left> < <right>
                <left> <= <right>
        """
        
        expression = self._make_term_expression()

        while not self._look_next().type == TokenType.EOF and self._match({
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL
        }):
            operator = self._prev()
            right = self._make_term_expression()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _make_term_expression(self) -> Expression.Expression:
        """
            Parses a term expression.
                <left> + <right>
                <left> - <right>
        """
        
        expression = self._make_factor_expression()

        while not self._look_next().type == TokenType.EOF and self._match({TokenType.MINUS, TokenType.PLUS}):
            operator = self._prev()
            right = self._make_factor_expression()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _make_factor_expression(self) -> Expression.Expression:
        """
            Parses a factor expression.
                <left> * <right>
                <left> / <right>
                <left> % <right>
        """
        
        expression = self._make_unary_expression()

        while not self._look_next().type == TokenType.EOF and self._match({TokenType.STAR, TokenType.SLASH, TokenType.PERCENT}):
            operator = self._prev()
            right = self._make_unary_expression()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _make_unary_expression(self) -> Expression.Expression:
        """
            Parses a unary expression.
                - <expression>
                ! <expression>
                ++ <variable>
                -- <variable>
        """
        
        if self._match({TokenType.MINUS, TokenType.NOT}):
            operator = self._prev()
            expression = self._make_unary_expression()
            return Expression.Unary(operator, expression)

        if self._match({TokenType.PLUS_PLUS, TokenType.MINUS_MINUS}):
            operator = self._prev()
            expression = self._make_unary_expression()

            if not isinstance(expression, Expression.Variable):
                raise SyntaxError(
                    f"Expected variable after prefix operator instead got '{expression}'")

            # TODO: checkear que funcione con var--
            return Expression.Assign(expression.name, Expression.Binary(expression, operator, Expression.Literal(1)))

        return self._make_postfix_expression()

    def _make_postfix_expression(self) -> Expression.Expression:
        """
            Parses a postfix expression.
                <variable>++
                <variable>--
        """
        
        expression = self._make_call_expression()

        if self._match({TokenType.PLUS_PLUS, TokenType.MINUS_MINUS}):
            operator = self._prev()

            if not isinstance(expression, Expression.Variable):
                raise SyntaxError(
                    f"Expected variable before postfix operator instead got '{expression}'")

            expression = Expression.Postfix(operator, expression)

        return expression

    def _make_call_expression(self) -> Expression.Expression:
        """
            Parses a call expression.
                <callee>(<arguments>)
        """
        
        expression = self._make_primary_expression()

        while self._match({TokenType.LEFT_PAREN}):
            arguments = []
            while not self._look_next().type in {TokenType.EOF, TokenType.RIGHT_PAREN}:
                arguments.append(self._make_expression())
                while not self._look_next().type == TokenType.EOF and self._match({TokenType.COMMA}):
                    arguments.append(self._make_expression())

                return Expression.Call(expression, arguments)

            if not self._match({TokenType.RIGHT_PAREN}):
                raise SyntaxError(
                    f"Expected '{TokenType.RIGHT_PAREN}' after arguments instead got '{self._look_next().type}'")

        return expression

    def _make_primary_expression(self) -> Expression.Expression:
        """
            Parses a primary expression.
                true
                false
                nil
                <number>
                <string>
                <identifier>
                (<expression>)
        """
        
        if self._match({TokenType.FALSE}):
            return Expression.Literal(False)
        if self._match({TokenType.TRUE}):
            return Expression.Literal(True)
        if self._match({TokenType.NIL}):
            return Expression.Literal(None)

        if self._match({TokenType.NUMBER, TokenType.STRING}):
            return Expression.Literal(self._prev().literal)

        if self._match({TokenType.IDENTIFIER}):
            return Expression.Variable(self._prev())

        if self._match({TokenType.LEFT_PAREN}):
            expression = self._make_expression()
            if not self._match({TokenType.RIGHT_PAREN}):
                raise SyntaxError(
                    f"Expected '{TokenType.RIGHT_PAREN}' after expression instead got '{self._look_next().type}'")
            return Expression.Group(expression)

        raise SyntaxError(
            f"Expected expression instead got '{self._look_next()}'")
