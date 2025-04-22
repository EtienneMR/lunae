"""
This module provides functionality for parsing expressions.
Expressions can include assignments or binary operations.
"""

from luma.language.ast.base.expr import Expr
from luma.parser.reader import ParserReader
from luma.tokenizer.grammar import TokenKind


def parse_expr(reader: ParserReader) -> Expr:
    """
    Parses an expression.

    Returns:
        Expr: The parsed expression.
    """
    from luma.parser.parsers.operations.binary import parse_binary
    from luma.parser.parsers.values.assign import parse_assign

    # Assignment vs binary
    if reader.is_followed(TokenKind.IDENT) and reader.is_followed(
        TokenKind.ASSIGN, offset=1
    ):
        return parse_assign(reader)
    return parse_binary(reader)
