from dataclasses import dataclass

from language.ast.base.statement import Statement


@dataclass
class Expr(Statement):
    """
    Base class for all expressions.
    """

    def __str__(self):
        return "EXPR"
