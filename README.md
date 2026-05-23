# lox-interpreter

Lox language interpreter coded in python

# How to run

```bash
uv venv && uv sync
source .venv/bin/activate
python3 lox <<file>>

# Run tests
uv pip install -e .
pytest
```

## Flags

- `--scan` prints the tokens of the program and exits
- `--parse` prints the AST of the program and exits
- `--resolve` shows the resolution of variables
- `--line-by-line` executes the file line by line, useful for debugging
- `file` if not provided, the interpreter will run in REPL mode

# Syntax

A detailed description of the syntax of the language can be found in the [lox specification](https://craftinginterpreters.com/the-lox-language.html#top). Some examples of lox + added syntax code can be found in the [examples](examples/) folder.

## Differences from canonical Lox

- Anonymous functions (lambdas): `fun (a, b) { return a + b; }` — function literals are first-class values (can be returned, assigned, passed as arguments).
- Power operator `**`: exponentiation (right-associative) — not in the original Lox spec.
- Increment/decrement: `++` and `--` supported as both prefix and postfix on variables.
- Ternary operator: conditional expressions using `? :`.
- Nested / multi-line comments: `/* ... */` with nesting support.

