"""
This module provides functionality for parsing numeric literals.
"""

from parser.reader import ParserReader

from language.ast.values.number import Number
from tokenizer.grammar import TokenKind


def parse_number(reader: ParserReader) -> Number:
    """
    Parses a numeric literal.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Number: The parsed numeric literal.
    """
    token = reader.expect(TokenKind.NUMBER)
    return Number(token.number_value)
