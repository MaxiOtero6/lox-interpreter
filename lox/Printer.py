from typing import List

from lox.Statement import Statement
from lox.utils import stringify

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"


def ast_to_string(statements: List[Statement]) -> str:
    if not statements:
        return ""

    lines: List[str] = []
    for i, stmt in enumerate(statements):
        is_last = i == len(statements) - 1
        lines.extend(_node_tree_lines(stmt, "", is_last, is_root=True))
    return "\n".join(lines)


def format_resolver_depths(depths: dict, color: bool = True) -> str:
    lines: List[str] = []
    header = _color("Resolver depths:", CYAN) if color else "Resolver depths:"
    lines.append(header)

    if not depths:
        empty = _color("  (no depths recorded)",
                       MAGENTA) if color else "  (no depths recorded)"
        lines.append(empty)
        return "\n".join(lines)

    for i, (node, depth) in enumerate(depths.items(), start=1):
        if hasattr(node, "ast_label"):
            node_label = node.ast_label()
        elif hasattr(node, "name") and hasattr(node.name, "lexeme"):
            node_label = node.name.lexeme
        else:
            node_label = str(node)

        # token
        if hasattr(node, "name") and hasattr(node.name, "lexeme") and hasattr(node.name, "type"):
            token_repr = _fmt_token(
                node.name) if color else f"{node.name.lexeme}:{node.name.type.name}"
        else:
            token_repr = _color(
                str(node_label), YELLOW) if color else str(node_label)

        depth_str = _color(str(depth), GREEN) if color else str(depth)

        lines.append(f"  {i}. {token_repr} -> depth: {depth_str}")

    return "\n".join(lines)


def format_tokens(tokens: list, color: bool = True) -> str:
    lines: List[str] = []
    header = _color("Tokens:", CYAN) if color else "Tokens:"
    lines.append(header)

    if not tokens:
        empty = _color("  (no tokens)", MAGENTA) if color else "  (no tokens)"
        lines.append(empty)
        return "\n".join(lines)

    lexemes = [t.lexeme for t in tokens if hasattr(t, "lexeme")]
    lex_w = max((len(l) for l in lexemes), default=6)

    for i, t in enumerate(tokens, start=1):
        line_no = getattr(t, "line", "?")
        lex = t.lexeme if hasattr(t, "lexeme") else str(t)
        typ = t.type.name if hasattr(t, "type") and hasattr(
            t.type, "name") else str(getattr(t, "type", ""))
        lit = getattr(t, "literal", None)

        if color:
            lex_fmt = _color(lex, YELLOW)
            typ_fmt = _color(typ, CYAN)
            lit_fmt = _fmt_literal(
                lit) if lit is not None else _color("nil", MAGENTA)
        else:
            lex_fmt = lex
            typ_fmt = typ
            lit_fmt = stringify(lit)

        row = f"  {i:>3}. [Line {line_no}] {lex_fmt:<{lex_w}} | {typ_fmt}"
        if lit is not None:
            row += f" = {lit_fmt}"
        lines.append(row)

    return "\n".join(lines)


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


def _color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


def _fmt_token(token) -> str:
    if hasattr(token, "lexeme") and hasattr(token, "type") and hasattr(token.type, "name"):
        return f"{_color(token.lexeme, YELLOW)}:{_color(token.type.name, CYAN)}"
    return str(token)


def _fmt_literal(value) -> str:
    return _color(stringify(value), GREEN)
