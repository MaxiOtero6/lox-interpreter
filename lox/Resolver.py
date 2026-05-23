from typing import Optional
import lox.Expression as Expression
from lox.Interpreter import Interpreter
import lox.Statement as Statement


class VariableInfo:
    def __init__(self, is_defined: bool, is_used: bool):
        self.is_defined = is_defined
        self.is_used = is_used


class Scope:
    def __init__(self):
        self.variables: dict[str, VariableInfo] = {}

    def define(self, name: str):
        self.variables[name] = VariableInfo(is_defined=True, is_used=False)

    def declare(self, name: str):
        if name in self.variables:
            raise RuntimeError(
                f"Variable '{name}' is already declared in this scope.")

        self.variables[name] = VariableInfo(is_defined=False, is_used=False)

    def use(self, name: str):
        if name in self.variables:
            self.variables[name].is_used = True
        else:
            raise RuntimeError(
                f"Variable '{name}' is not defined in this scope.")

    def is_defined(self, name: str) -> bool:
        return name in self.variables and self.variables[name].is_defined

    def is_used(self, name: str) -> bool:
        return name in self.variables and self.variables[name].is_used

    def get(self, name: str) -> Optional[VariableInfo]:
        if name in self.variables:
            return self.variables[name]

        return None


class Resolver():
    def __init__(self, interpreter: Interpreter) -> None:
        self.scopes: list[Scope] = []
        self.interpreter = interpreter

    def resolve(self, argument: Statement.Statement | Expression.Expression):
        match argument:
            case Statement.Statement():
                self._resolve_statement(argument)
            case Expression.Expression():
                self._resolve_expression(argument)

    def _resolve_statement(self, statement: Statement.Statement):
        match statement:
            case Statement.If() as if_stmt:
                self.resolve(if_stmt.condition)
                self.resolve(if_stmt.then_branch)
                if if_stmt.else_branch is not None:
                    self.resolve(if_stmt.else_branch)

            case Statement.FunctionDeclaration() as function:
                self._declare(function.name.lexeme)
                self._define(function.name.lexeme)
                self._begin_scope()
                for param in function.params:
                    self._declare(param.lexeme)
                    self._define(param.lexeme)
                for s in function.body:
                    self.resolve(s)
                self._end_scope()

            case Statement.While() as while_stmt:
                self.resolve(while_stmt.condition)
                self.resolve(while_stmt.body)

            case Statement.Return() as return_stmt:
                if return_stmt.value is not None:
                    self.resolve(return_stmt.value)

            case Statement.Print() as print_stmt:
                self.resolve(print_stmt.expression)

            case Statement.Expression() as expression_stmt:
                self.resolve(expression_stmt.expression)

            case Statement.VariableDeclaration() as var_stmt:
                self._declare(var_stmt.name.lexeme)
                if var_stmt.initializer is not None:
                    self.resolve(var_stmt.initializer)
                self._define(var_stmt.name.lexeme)

            case Statement.Block() as block_stmt:
                self._begin_scope()
                for s in block_stmt.statements:
                    self._resolve_statement(s)
                self._end_scope()

            case _:
                raise NotImplementedError(
                    f"Statement type {type(statement)} not implemented"
                )

    def _resolve_expression(self, expression: Expression.Expression):
        match expression:
            case Expression.Postfix() as postfix:
                self.resolve(postfix.left)

            case Expression.Prefix() as prefix:
                self.resolve(prefix.right)

            case Expression.Logic() as logic:
                self.resolve(logic.left)
                self.resolve(logic.right)

            case Expression.Unary() as unary:
                self.resolve(unary.right)

            case Expression.Group() as group:
                self.resolve(group.expression)

            case Expression.Ternary() as ternary:
                self.resolve(ternary.condition)
                self.resolve(ternary.true_expr)
                self.resolve(ternary.false_expr)

            case Expression.Call() as call:
                self.resolve(call.callee)
                for argument in call.arguments:
                    self.resolve(argument)

            case Expression.Binary() as binary:
                self.resolve(binary.left)
                self.resolve(binary.right)

            case Expression.Literal():
                return

            case Expression.Variable() as variable:
                if not self.scopes:
                    return

                info = self.scopes[-1].get(variable.name.lexeme)
                if info is not None and not info.is_defined:
                    raise RuntimeError(
                        f"Cannot read variable '{variable.name.lexeme}' in its own initializer."
                    )

                depth = self._search_depth(variable.name.lexeme)
                if depth is not None:
                    self.interpreter.set_depth(variable, depth)
                    for i in range(len(self.scopes) - 1, -1, -1):
                        if self.scopes[i].is_defined(variable.name.lexeme):
                            self.scopes[i].use(variable.name.lexeme)
                            break

            case Expression.Assign() as assignment:
                value = self.resolve(assignment.value)

                if not self.scopes:
                    return value

                depth = self._search_depth(assignment.name.lexeme)
                if depth is not None:
                    self.interpreter.set_depth(assignment, depth)

                return value

            case _:
                raise NotImplementedError(
                    f"Expression type {type(expression)} not implemented"
                )

    def _begin_scope(self):
        self.scopes.append(Scope())

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name: str):
        if not self.scopes:
            return

        self.scopes[-1].declare(name)

    def _define(self, name: str):
        if not self.scopes:
            return

        self.scopes[-1].define(name)

    def _search_depth(self, name: str) -> int | None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if self.scopes[i].is_defined(name):
                return len(self.scopes) - 1 - i
        return None
