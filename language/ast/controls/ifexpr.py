from dataclasses import dataclass
from typing import Optional

from language.ast.base.expr import Expr
from language.ast.base.statement import Statement
from utils.indent import indent


@dataclass
class IfExpr(Expr):
    """
    Represents an if-expression.

    Attributes:
        cond (Expr): The condition expression.
        then_branch (Expr): The expression for the 'then' branch.
        else_branch (Optional[Expr]): The expression for the 'else' branch, if any.
    """

    cond: Expr
    then_branch: Statement
    else_branch: Optional[Statement]

    def __str__(self) -> str:
        """
        Returns a string representation of the if-expression.

        Returns:
            str: The string representation of the if-expression.
        """
        return f"IF\n{indent(self.cond)}\n{indent(self.then_branch)}\n{indent(self.else_branch)}"
