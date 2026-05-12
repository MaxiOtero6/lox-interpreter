from typing import Optional


class Environment:
    values: dict[str, object]
    enclosing: Optional["Environment"]
    
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def ancestor(self, distance: int) -> "Environment":
        environment = self
        for _ in range(distance):
            if environment.enclosing is None:
                raise RuntimeError("No enclosing environment at the specified distance.")
            environment = environment.enclosing
        return environment

    def get(self, name: str, depth: int = 0) -> object:
        if depth is not None:
            return self.ancestor(depth).get(name)

        if name in self.values:
            return self.values[name]
        
        raise RuntimeError(f"Undefined variable '{name}'.")

    def assign(self, name: str, value: object, depth: int = 0) -> object:
        if depth is not None:
            return self.ancestor(depth).assign(name, value)

        if name in self.values:
            self.values[name] = value
            return value
        
        raise RuntimeError(f"Undefined variable '{name}'.")