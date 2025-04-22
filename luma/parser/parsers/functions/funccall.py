"""
This module provides functionality for parsing function calls.
"""

from luma.language.ast.base.expr import Expr
from luma.language.ast.functions.funccall import FuncCall
from luma.parser.parsers.base.expr import parse_expr
from luma.parser.reader import ParserReader
from luma.tokenizer.grammar import TokenKind


def parse_func_call(reader: ParserReader, name: str) -> FuncCall:
    """
    Parses a function call.

    Args:
        reader (ParserReader): The parser reader instance.
        name (str): The name of the function being called.

    Returns:
        FuncCall: The parsed function call.
    """
    reader.expect(TokenKind.LPAREN)

    args: list[Expr] = []

    if not reader.match(TokenKind.RPAREN):
        while True:
            args.append(parse_expr(reader))
            if reader.match(TokenKind.RPAREN):
                break
            reader.expect(TokenKind.COMMA)

    return FuncCall(name, args)
