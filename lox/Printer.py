def stringify(value: object) -> str:
    """Golden rule"""
    if value is None:
        return "nil"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
