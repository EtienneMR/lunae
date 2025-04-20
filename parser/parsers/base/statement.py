from parser.parsers.base.expr import parse_expr
from parser.reader import ParserReader

from language.ast.base.statement import Statement
from tokenizer.grammar import TokenKind


def parse_statement(reader: ParserReader) -> Statement:
    """
    Parses a single statement.

    Returns:
        Statement: The parsed statement.
    """
    from parser.parsers.functions.funcdef import parse_func_def

    # Function definition
    if reader.is_followed(TokenKind.KEYWORD, "func"):
        return parse_func_def(reader)
    expr = parse_expr(reader)
    reader.match(TokenKind.NEWLINE)
    return expr
