from dataclasses import dataclass

from language.ast.base.expr import Expr
from language.ast.base.statement import Statement
from utils.indent import indent


@dataclass
class Block(Expr):
    """
    Represents a block of statements.

    Attributes:
        statements (list[Expr]): The list of statements in the block.
    """

    statements: list[Statement]

    def __str__(self):
        return f"BLOCK\n{'\n'.join(indent(s) for s in self.statements)}"
