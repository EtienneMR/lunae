from typing import Any, Optional


class Environment:

    def __init__(self, parent: "Optional[Environment]" = None):
        self.vars: dict[str, Any] = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable '{name}'")

    def set(self, name, value):
        self.vars[name] = value

    def define(self, name, value):
        self.vars[name] = value
