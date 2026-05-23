from typing import List

from lox.Statement import Statement

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"


def stringify(value: object) -> str:
    """Golden rule"""
    if value is None:
        return "nil"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def ast_to_string(statements: List[Statement]) -> str:
    if not statements:
        return ""

    lines: List[str] = []
    for i, stmt in enumerate(statements):
        is_last = i == len(statements) - 1
        lines.extend(_node_tree_lines(stmt, "", is_last, is_root=True))
    return "\n".join(lines)


def _color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


def _fmt_token(token) -> str:
    try:
        lex = token.lexeme
        tname = token.type.name
        return f"{_color(lex, YELLOW)}:{_color(tname, CYAN)}"
    except Exception:
        return str(token)


def _fmt_literal(value) -> str:
    return _color(stringify(value), GREEN)


def _node_tree_lines(node, prefix: str, is_last: bool, is_root: bool = False) -> List[str]:
    connector = "" if is_root and prefix == "" else (
        "└── " if is_last else "├── ")

    if hasattr(node, "ast_label"):
        raw_label = node.ast_label()
        label = _color(raw_label, BOLD)
    elif hasattr(node, "lexeme") and hasattr(node, "type"):
        label = _fmt_token(node)
    else:
        label = str(node)

    lines: List[str] = [f"{prefix}{connector}{label}"]

    children = []
    if hasattr(node, "ast_children"):
        children = node.ast_children() or []

    for idx, child in enumerate(children):
        if child is None:
            continue
        child_is_last = idx == len(children) - 1
        child_prefix = prefix + ("    " if is_last else "│   ")

        # node child
        if hasattr(child, "ast_label"):
            lines.extend(_node_tree_lines(child, child_prefix, child_is_last))
            continue

        # token child
        if hasattr(child, "lexeme") and hasattr(child, "type"):
            conn = "└── " if child_is_last else "├── "
            lines.append(f"{child_prefix}{conn}{_fmt_token(child)}")
            continue

        # primitive
        if isinstance(child, str):
            conn = "└── " if child_is_last else "├── "
            lines.append(f"{child_prefix}{conn}{_color(child, MAGENTA)}")
            continue

        # literal value
        conn = "└── " if child_is_last else "├── "
        lines.append(f"{child_prefix}{conn}{_fmt_literal(child)}")

    return lines
