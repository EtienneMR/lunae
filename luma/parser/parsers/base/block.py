"""
This module provides functionality for parsing blocks of statements or expressions.
Blocks can be multi-line (indented) or single-line.
"""

from luma.language.ast.base.block import Block
from luma.language.ast.base.expr import Expr
from luma.parser.parsers.base.expr import parse_expr
from luma.parser.parsers.base.statement import parse_statement
from luma.parser.reader import ParserReader
from luma.tokenizer.grammar import TokenKind


def parse_block(reader: ParserReader) -> Block | Expr:
    """
    Parses a block of statements or a single-line expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Block | Expr: The parsed block or single expr.
    """
    if reader.match(TokenKind.NEWLINE) and reader.is_followed(TokenKind.INDENT):
        reader.expect(TokenKind.INDENT)
        statements: list[Expr] = []
        while not reader.match(TokenKind.DEDENT):
            if reader.match(TokenKind.NEWLINE):
                continue
            statements.append(parse_statement(reader))

        # same behavior
        if len(statements) == 1:
            return statements[0]
        return Block(statements)
    # single-line expression
    expr = parse_expr(reader)
    reader.match(TokenKind.NEWLINE)
    return expr


def parse_reader(reader: ParserReader) -> Block:
    """
    Parses the entire input from the reader into a block of statements.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Block: The parsed block of statements.
    """
    statements: list[Expr] = []
    while reader.peek():
        if reader.match(TokenKind.NEWLINE):
            continue
        statements.append(parse_statement(reader))
    return Block(statements)
