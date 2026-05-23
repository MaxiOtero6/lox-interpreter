import argparse
from enum import Enum

try:
    from prompt_toolkit import PromptSession
except Exception:
    PromptSession = None

from lox.Interpreter import Interpreter
from lox.Parser import Parser
from lox.Resolver import Resolver
from lox.Scanner import Scanner
from lox.Statement.Statement import Statement
from lox.Token.Token import Token


class _LoxMode(Enum):
    SCAN = 1
    PARSE = 2
    RESOLVE = 3
    FULL = 4  # scan, parse, resolve, and interpret


class Lox:
    def __init__(self):
        self.session = PromptSession() if PromptSession is not None else None
        self.args = self._get_args()
        self.mode = _LoxMode.FULL

    def _get_args(self):
        parser = argparse.ArgumentParser(
            prog="lox", description="Lox Interpreter")

        parser.add_argument(
            "--scan", action="store_true", help="Run the scanner and print the tokens"
        )
        parser.add_argument(
            "--parse", action="store_true", help="Run the parser and print the AST"
        )
        parser.add_argument(
            "--resolve",
            action="store_true",
            help="Run the resolver and print the resolved AST",
        )
        parser.add_argument(
            "file", nargs="?", help="Lox source file to execute instead of REPL"
        )
        parser.add_argument(
            "--line-by-line", action="store_true", help="Run in line-by-line mode"
        )

        args = parser.parse_args()
        args.repl = not args.file
        return args

    def _scan(self, source: str) -> list[Token]:
        scanner = Scanner()
        try:
            return scanner.scan(source)
        except Exception as e:
            raise RuntimeError(f"Scanner error: {e}")

    def _parse(self, tokens: list[Token]) -> list[Statement]:
        parser = Parser(tokens)
        try:
            return parser.parse()
        except Exception as e:
            raise RuntimeError(f"Parser error: {e}")

    def _resolve(self, statements: list[Statement], interpreter: Interpreter):
        resolver = Resolver(interpreter)
        try:
            for s in statements:
                resolver.resolve(s)
        except Exception as e:
            raise RuntimeError(f"Resolver error: {e}")

    def _interpret(self, statements: list[Statement], interpreter: Interpreter):
        try:
            return interpreter.interpret(statements)
        except Exception as e:
            raise RuntimeError(f"Runtime error: {e}")

    def _run(self, source: str):
        try:
            tokens = self._scan(source)
            if self.mode == _LoxMode.SCAN:
                for token in tokens:
                    print(token)
                return

            statements = self._parse(tokens)
            if self.mode == _LoxMode.PARSE:
                for statement in statements:
                    print(statement)
                return

            interpreter = Interpreter()
            self._resolve(statements, interpreter)

            result = self._interpret(statements, interpreter)
            if self.args.repl and result is not None:
                print(result)
        except RuntimeError as e:
            print(f"\033[31m{e}\033[0m")

    def run(self):
        if self.args.scan:
            self.mode = _LoxMode.SCAN
        elif self.args.parse:
            self.mode = _LoxMode.PARSE
        elif self.args.resolve:
            self.mode = _LoxMode.RESOLVE

        if self.args.file:
            with open(self.args.file, "r") as f:
                if self.args.line_by_line:
                    for line in f:
                        print(f"> {line.strip()}")
                        self._run(line)
                else:
                    file: str = f.read()
                    self._run(file)
            return

        while True:
            try:
                if self.session is not None:
                    line = str(self.session.prompt(">>> "))
                else:
                    line = input(">>> ")
                self._run(line)
            except (EOFError, KeyboardInterrupt):
                break
