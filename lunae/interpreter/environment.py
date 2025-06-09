"""
This module defines the Environment class used for managing variable scopes and bindings.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from lunae.language.typesystem import Type
from lunae.utils.errors import InterpreterError


@dataclass(frozen=True)
class Cell:
    value: Any
    type: Type


@dataclass
class Binding:
    cell: Cell
    mutable: bool = True


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.bindings: Dict[str, Binding] = {}

    def define(self, name: str, binding: Binding) -> None:
        """Introduce a new name in this scope."""
        if name in self.bindings:
            raise NameError(f"Name '{name}' already defined in this scope")
        self.bindings[name] = binding

    def resolve(self, name: str) -> Binding:
        """Retrieve a binding from it's name, walking up scopes."""
        env: Optional[Environment] = self
        while env:
            if name in env.bindings:
                return env.bindings[name]
            env = env.parent
        raise NameError(f"Name '{name}' is not defined")

    def set(self, name: str, cell: Cell) -> None:
        """Assign to an existing binding, walking up scopes."""
        binding = self.resolve(name)
        if not binding.mutable:
            raise TypeError(f"Cannot assign to immutable '{name}'")
        binding.cell = cell

    def get(self, name: str) -> Cell:
        """Retrieve a binding’s cell, walking up scopes."""
        return self.resolve(name).cell
