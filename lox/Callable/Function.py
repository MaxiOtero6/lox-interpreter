from typing import TYPE_CHECKING

from lox.Environment import Environment
from lox.Statement.FunctionDeclaration import FunctionDeclaration
from lox.Statement.Statement import Statement

from .ReturnException import ReturnException

if TYPE_CHECKING:
    from lox.Interpreter import Interpreter


class Function:
    def __init__(self, declaration: FunctionDeclaration, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def __call__(self, interpreter: "Interpreter", arguments: list[Statement]):
        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as returnValue:
            return returnValue.value

    def __str__(self) -> str:
        params = ', '.join(param.lexeme for param in self.declaration.params) 
        return f"<fn {self.declaration.name.lexeme}({params})>>"
