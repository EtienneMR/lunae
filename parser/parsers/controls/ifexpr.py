"""
This module provides the parser for if-expressions.
"""

from parser.parsers.base.block import parse_block
from parser.parsers.base.expr import parse_expr
from parser.reader import ParserReader
from typing import Optional

from language.ast.base.expr import Expr
from language.ast.base.statement import Statement
from language.ast.controls.ifexpr import IfExpr
from tokenizer.grammar import TokenKind


def parse_if_expr(reader: ParserReader) -> IfExpr:
    """
    Parses an if-expression.

    Args:
        reader (ParserReader): The parser reader.

    Returns:
        IfExpr: The parsed if-expression node.
    """
    reader.expect(TokenKind.KEYWORD, "if")
    cond = parse_expr(reader)
    reader.expect(TokenKind.COLON)
    then_branch = parse_block(reader)
    else_branch: Optional[Statement] = None
    if reader.match(TokenKind.KEYWORD, "else"):
        reader.expect(TokenKind.COLON)
        else_branch = parse_block(reader)
    return IfExpr(cond, then_branch, else_branch)
