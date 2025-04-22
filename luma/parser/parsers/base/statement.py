"""
This module provides functionality for parsing statements in the language.
Statements can include function definitions or expressions.
"""

from luma.language.ast.base.expr import Expr
from luma.parser.parsers.base.expr import parse_expr
from luma.parser.reader import ParserReader
from luma.tokenizer.grammar import TokenKind


def parse_statement(reader: ParserReader) -> Expr:
    """
    Parses a single expr, which can be a function definition or an expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Expr: The parsed expr.
    """
    from luma.parser.parsers.functions.funcdef import parse_func_def

    # Function definition
    if reader.is_followed(TokenKind.KEYWORD, "func"):
        return parse_func_def(reader)
    expr = parse_expr(reader)
    reader.match(TokenKind.NEWLINE)
    return expr
