"""
This module provides functionality for parsing assignment expressions.
"""

from parser.parsers.base.expr import parse_expr
from parser.reader import ParserReader

from language.ast.values.assign import Assign
from tokenizer.grammar import TokenKind


def parse_assign(reader: ParserReader) -> Assign:
    """
    Parses an assignment expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Assign: The parsed assignment expression.
    """
    name = reader.expect(TokenKind.IDENT).match
    reader.expect(TokenKind.ASSIGN)
    value = parse_expr(reader)
    return Assign(name, value)
