"""
This module provides functionality for parsing while expressions.
"""

from parser.parsers.base.block import parse_block
from parser.parsers.base.expr import parse_expr
from parser.reader import ParserReader

from language.ast.controls.whileexpr import WhileExpr
from tokenizer.grammar import TokenKind


def parse_while_expr(reader: ParserReader) -> WhileExpr:
    """
    Parses a while expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        WhileExpr: The parsed while expression.
    """
    reader.expect(TokenKind.KEYWORD, "while")
    cond = parse_expr(reader)
    reader.expect(TokenKind.COLON)
    body = parse_block(reader)
    return WhileExpr(cond, body)
