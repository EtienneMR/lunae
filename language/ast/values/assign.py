from dataclasses import dataclass

from language.ast.base.expr import Expr
from language.ast.base.statement import Statement
from utils.indent import indent


@dataclass
class Assign(Statement):
    """
    Represents an assignment statement.

    Attributes:
        name (str): The variable name.
        value (Expr): The value to assign.
    """

    name: str
    value: Expr

    def __str__(self):
        return f"ASSIGN {self.name!r}\n{indent(self.value)}"
