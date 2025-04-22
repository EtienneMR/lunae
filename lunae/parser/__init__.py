"""
This module provides the main parsing functionality for the language.
It converts tokens into an abstract syntax tree (AST).
"""

from lunae.language.ast.base.block import Block
from lunae.parser.parsers.base.block import parse_reader
from lunae.parser.reader import ParserReader
from lunae.tokenizer import Token


def parse(toknes: list[Token]) -> Block:
    """
    Parses a list of tokens into an abstract syntax tree (AST).

    Args:
        toknes (list[Token]): The list of tokens to parse.

    Returns:
        Block: The root block of the parsed AST.
    """
    reader = ParserReader(toknes)
    ast = parse_reader(reader)
    return ast


__all__ = ("parse",)
