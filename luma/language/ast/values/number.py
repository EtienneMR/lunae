from dataclasses import dataclass

from luma.language.ast.base.expr import Expr


@dataclass
class Number(Expr):
    """
    Represents a numeric literal.

    Attributes:
        value (float): The numeric value.
    """

    value: float

    def __str__(self):
        return f"NUMBER {self.value!r}"
