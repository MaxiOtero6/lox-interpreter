from typing import Any


def stringify(value: Any) -> str:
    """
    Golden rule: Convert a Python value to its representation for Lox.
    """
    if value is None:
        return "nil"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return f"[{', '.join(stringify(element) for element in value)}]"
    return str(value)
