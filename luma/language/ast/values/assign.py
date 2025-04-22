"""
This module defines the Assign class, which represents an assignment expr in the AST.
"""

from dataclasses import dataclass

from luma.language.ast.base.expr import Expr
from luma.utils.indent import indent


@dataclass
class Assign(Expr):
    """
    Represents an assignment expr.

    Attributes:
        name (str): The variable name.
        value (Expr): The value to assign.
    """

    name: str
    value: Expr

    def __str__(self):
        return f"ASSIGN {self.name!r}\n{indent(self.value)}"
