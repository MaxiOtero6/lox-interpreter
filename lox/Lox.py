import argparse
from enum import Enum

from prompt_toolkit import PromptSession

from lox.Scanner import Scanner
from lox.Parser import Parser
from lox.Resolver import Resolver
from lox.Interpreter import Interpreter


class _LoxMode(Enum):
    SCAN = 1
    PARSE = 2
    RESOLVE = 3
    FULL = 4  # scan, parse, resolve, and interpret


class Lox:
    def __init__(self):
        self.session = PromptSession()
        self.args = self._get_args()
        self.mode = _LoxMode.FULL

    def _get_args(self):
        parser = argparse.ArgumentParser(
            prog="lox",
            description="Lox Interpreter"
        )

        parser.add_argument(
            "--scan",
            action="store_true",
            help="Run the scanner and print the tokens"
        )
        parser.add_argument(
            "--parse",
            action="store_true",
            help="Run the parser and print the AST"
        )
        parser.add_argument(
            "--resolve",
            action="store_true",
            help="Run the resolver and print the resolved AST"
        )
        parser.add_argument(
            "file",
            nargs="?",
            help="Lox source file to execute instead of REPL"
        )

        return parser.parse_args()

    def _run(self, source: str):
        scanner = Scanner()
        parser = Parser()
        resolver = Resolver()
        interpreter = Interpreter()

    def run(self):
        if self.args.scan:
            self.mode = _LoxMode.SCAN
        elif self.args.parse:
            self.mode = _LoxMode.PARSE
        elif self.args.resolve:
            self.mode = _LoxMode.RESOLVE

        if self.args.file:
            with open(self.args.file, "r") as f:
                file: str = f.read()
                self._run(file)
            return

        while True:
            try:
                line = str(self.session.prompt(">>> "))
                self._run(line)
            except (EOFError, KeyboardInterrupt):
                break
