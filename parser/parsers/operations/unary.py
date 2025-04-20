"""
This module provides functionality for parsing unary operations.
"""

from parser.parsers.base.primary import parse_primary
from parser.reader import ParserReader

from language.ast.base.expr import Expr
from language.ast.functions.funccall import FuncCall
from language.syntax import UNARY_OPERATORS
from tokenizer.grammar import TokenKind


def parse_unary(reader: ParserReader) -> FuncCall | Expr:
    """
    Parses a unary operation or a primary expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        FuncCall | Expr: The parsed unary operation or primary expression.
    """
    tok = reader.peek()
    if tok and tok.kind == TokenKind.OP and tok.match in UNARY_OPERATORS:
        op = UNARY_OPERATORS[tok.match]
        reader.skip()
        operand = parse_unary(reader)
        return FuncCall(op.function, [operand])
    return parse_primary(reader)
