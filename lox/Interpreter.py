import lox.Expression as Expression
import lox.Statement as Statement
from lox.Callable import ReturnException
from lox.Environment import Environment
from lox.Token import TokenType
from lox.Token.Token import Token
from lox.Callable.Function import Function
from lox.utils import stringify


class Interpreter:
    global_env: Environment
    current_env: Environment
    depths: dict[Expression.Variable | Expression.Assign, int]

    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.depths = {}

    def interpret(self, statements: list[Statement.Statement]):
        value = None
        for s in statements:
            value = self.execute(s)

        return value

    def set_depth(self, expression: Expression.Variable | Expression.Assign, depth: int):
        self.depths[expression] = depth

    def execute(self, statement: Statement.Statement):
        match statement:
            case Statement.If() as if_stmt:
                if self.evaluate(if_stmt.condition):
                    return self.execute(if_stmt.then_branch)
                elif if_stmt.else_branch is not None:
                    return self.execute(if_stmt.else_branch)
                return

            case Statement.FunctionDeclaration() as function:
                func_obj = Function(function, self.current_env)
                self.current_env.define(function.name.lexeme, func_obj)
                return None

            case Statement.While() as while_stmt:
                while self.evaluate(while_stmt.condition):
                    self.execute(while_stmt.body)
                return

            case Statement.Return() as return_stmt:
                value = None
                if return_stmt.value is not None:
                    value = self.evaluate(return_stmt.value)
                raise ReturnException(value)

            case Statement.Print() as print_stmt:
                value = self.evaluate(print_stmt.expression)
                print(stringify(value))
                return None

            case Statement.Expression() as expression_stmt:
                return self.evaluate(expression_stmt.expression)

            case Statement.VariableDeclaration() as var_stmt:
                value = None
                if var_stmt.initializer is not None:
                    value = self.evaluate(var_stmt.initializer)
                self.current_env.define(var_stmt.name.lexeme, value)
                return value

            case Statement.Block() as block_stmt:
                self.execute_block(block_stmt.statements,
                                   Environment(self.current_env))

            case _:
                raise NotImplementedError(
                    f"Statement type {type(statement)} not implemented"
                )

    def evaluate(self, expression: Expression.Expression):
        match expression:
            case Expression.Postfix() as postfix:
                if not isinstance(postfix.left, Expression.Variable):
                    raise RuntimeError(
                        "Postfix operator can only be applied to variables"
                    )

                old_value = (
                    self.current_env.get(
                        postfix.left.name.lexeme, self.depths[postfix.left]
                    )
                    if postfix.left in self.depths
                    else self.global_env.get(postfix.left.name.lexeme)
                )

                if not isinstance(old_value, (int, float)):
                    raise RuntimeError(
                        f"Operand must be a number, got {type(old_value)}")

                match postfix.operator.type:
                    case TokenType.PLUS_PLUS:
                        value = old_value + 1
                    case TokenType.MINUS_MINUS:
                        value = old_value - 1
                    case _:
                        raise NotImplementedError(
                            f"Postfix operator {postfix.operator.type} not implemented"
                        )

                if postfix.left in self.depths:
                    self.current_env.assign(
                        postfix.left.name.lexeme, value, self.depths[postfix.left]
                    )
                else:
                    self.global_env.assign(postfix.left.name.lexeme, value)

                return old_value

            case Expression.Prefix() as prefix:
                # Variable: modify in place and return new value
                if isinstance(prefix.right, Expression.Variable):
                    var = prefix.right
                    old_value = (
                        self.current_env.get(var.name.lexeme, self.depths[var])
                        if var in self.depths
                        else self.global_env.get(var.name.lexeme)
                    )

                    if not isinstance(old_value, (int, float)):
                        raise RuntimeError(
                            f"Operand must be a number, got {type(old_value)}"
                        )

                    match prefix.operator.type:
                        case TokenType.PLUS_PLUS:
                            value = old_value + 1
                        case TokenType.MINUS_MINUS:
                            value = old_value - 1
                        case _:
                            raise NotImplementedError(
                                f"Prefix operator {prefix.operator.type} not implemented"
                            )

                    if var in self.depths:
                        self.current_env.assign(
                            var.name.lexeme, value, self.depths[var])
                    else:
                        self.global_env.assign(var.name.lexeme, value)

                    return value

                # Non-variable: evaluate right side and compute increment/decrement
                right_val = self.evaluate(prefix.right)
                if not isinstance(right_val, (int, float)):
                    raise RuntimeError(
                        f"Operand must be a number, got {type(right_val)}")

                match prefix.operator.type:
                    case TokenType.PLUS_PLUS:
                        return right_val + 1
                    case TokenType.MINUS_MINUS:
                        return right_val - 1
                    case _:
                        raise NotImplementedError(
                            f"Prefix operator {prefix.operator.type} not implemented"
                        )

            case Expression.Logic() as logic:
                left = self.evaluate(logic.left)

                match logic.operator.type:
                    case TokenType.OR:
                        if left:
                            return left
                    case TokenType.AND:
                        if not left:
                            return left

                return self.evaluate(logic.right)

            case Expression.Unary() as unary:
                right = self.evaluate(unary.right)
                match unary.operator.type:
                    case TokenType.MINUS:
                        if not isinstance(right, (int, float)):
                            raise RuntimeError(
                                f"Operand must be a number, got {type(right)}"
                            )
                        return -right

                    case TokenType.NOT:
                        return not bool(right)
                    case _:
                        raise NotImplementedError(
                            f"Unary operator {unary.operator.type} not implemented"
                        )

            case Expression.Group() as group:
                return self.evaluate(group.expression)

            case Expression.Ternary() as ternary:
                return (
                    self.evaluate(ternary.true_expr)
                    if self.evaluate(ternary.condition)
                    else self.evaluate(ternary.false_expr)
                )

            case Expression.Call() as call:
                callee = self.evaluate(call.callee)
                arguments = [self.evaluate(arg) for arg in call.arguments]

                if not isinstance(callee, Function):
                    raise RuntimeError(
                        f"Can only call functions, got '{str(callee)}'")

                if len(arguments) != callee.arity():
                    raise RuntimeError(
                        f"Expected {callee.arity()} arguments, got {len(arguments)}"
                    )

                return callee(self, arguments)

            case Expression.Function() as func_expr:
                name_token = Token(TokenType.IDENTIFIER, "<anon>", None,
                                   func_expr.params[0].line if func_expr.params else 0)
                func_decl = Statement.FunctionDeclaration(
                    name_token, func_expr.params, func_expr.body)
                return Function(func_decl, self.current_env)

            case Expression.Binary() as binary:
                left = self.evaluate(binary.left)
                right = self.evaluate(binary.right)

                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    match binary.operator.type:
                        case TokenType.PLUS:
                            return left + right
                        case TokenType.MINUS:
                            return left - right
                        case TokenType.STAR:
                            return left * right
                        case TokenType.SLASH:
                            return left / right
                        case TokenType.PERCENT:
                            return left % right
                        case TokenType.STAR_STAR:
                            return left ** right
                        case TokenType.GREATER:
                            return left > right
                        case TokenType.GREATER_EQUAL:
                            return left >= right
                        case TokenType.LESS:
                            return left < right
                        case TokenType.LESS_EQUAL:
                            return left <= right

                if isinstance(left, str) and isinstance(right, str) and binary.operator.type == TokenType.PLUS:
                    return left + right

                match binary.operator.type:
                    case TokenType.EQUAL_EQUAL:
                        return left == right
                    case TokenType.BANG_EQUAL:
                        return left != right

                if binary.operator.type == TokenType.PLUS:
                    raise RuntimeError(
                        "Operands of + must be either numbers or strings")
                raise NotImplementedError(
                    f"Binary operator {binary.operator.type} not implemented"
                )

            case Expression.ListLiteral() as list_literal:
                return [self.evaluate(element) for element in list_literal.elements]

            case Expression.IndexGet() as index_get:
                collection = self.evaluate(index_get.collection)
                index = self._normalize_index(self.evaluate(index_get.index))
                self._check_indexable(collection)
                self._check_index_bounds(collection, index)
                return collection[index]

            case Expression.IndexSet() as index_set:
                collection = self.evaluate(index_set.collection)
                index = self._normalize_index(self.evaluate(index_set.index))
                self._check_indexable(collection)

                if isinstance(collection, str):
                    raise RuntimeError("Cannot assign to string index")

                self._check_index_bounds(collection, index)
                value = self.evaluate(index_set.value)
                collection[index] = value
                return value

            case Expression.Literal() as literal:
                return literal.value

            case Expression.Variable() as variable:
                if variable in self.depths:
                    return self.current_env.get(
                        variable.name.lexeme, self.depths[variable]
                    )
                return self.global_env.get(variable.name.lexeme)

            case Expression.Assign() as assignment:
                value = self.evaluate(assignment.value)

                if assignment in self.depths:
                    self.current_env.assign(
                        assignment.name.lexeme, value, self.depths[assignment]
                    )
                    return value

                self.global_env.assign(assignment.name.lexeme, value)
                return value

            case _:
                raise NotImplementedError(
                    f"Expression type {type(expression)} not implemented"
                )

    def _normalize_index(self, index: object) -> int:
        if not isinstance(index, (int, float)) or isinstance(index, bool):
            raise RuntimeError(f"Index must be a number, got {type(index)}")

        if int(index) != index:
            raise RuntimeError(f"Index must be an integer, got {index}")

        return int(index)

    def _check_indexable(self, collection: object) -> None:
        if not isinstance(collection, (list, str)):
            raise RuntimeError(
                f"Can only index lists and strings, got {type(collection)}")

    def _check_index_bounds(self, collection: list | str, index: int) -> None:
        if index < 0 or index >= len(collection):
            raise RuntimeError(
                f"Index {index} out of bounds for length {len(collection)}")

    def execute_block(
        self, statements: list[Statement.Statement], environment: Environment
    ):
        previous_env = self.current_env
        self.current_env = environment
        try:
            return self.interpret(statements)
        finally:
            self.current_env = previous_env
