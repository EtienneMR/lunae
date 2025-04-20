from parser.parsers.base.expr import parse_expr
from parser.parsers.controls import CONTROL_EXPRESSIONS
from parser.parsers.values.number import parse_number
from parser.parsers.values.string import parse_string
from parser.parsers.values.var import parse_var
from parser.reader import ParserReader

from language.ast.base.expr import Expr
from tokenizer.grammar import TokenKind
from utils.errors import ParserError


def parse_primary(reader: ParserReader) -> Expr:
    """
    Parses a primary expression.

    Returns:
        Expr: The parsed expression.

    Raises:
        ParserError: If an unexpected token is encountered.
    """

    tok = reader.peek()
    if not tok:
        raise ParserError("Unexpected end of file", None, None)

    if tok.kind == TokenKind.NUMBER:
        return parse_number(reader)
    if tok.kind == TokenKind.STRING:
        return parse_string(reader)
    if tok.kind == TokenKind.IDENT:
        return parse_var(reader)

    # Parenthesized
    if tok.kind == TokenKind.LPAREN:
        reader.expect(TokenKind.LPAREN)
        expr = parse_expr(reader)
        reader.expect(TokenKind.RPAREN)
        return expr

    if tok.kind == TokenKind.KEYWORD:
        if tok.match not in CONTROL_EXPRESSIONS:
            raise ParserError(
                f"Unexpected control keyword: {tok.match!r}", tok.start, tok.end
            )
        expression = CONTROL_EXPRESSIONS[tok.match]
        return expression(reader)

    raise ParserError(f"Unexpected token: {tok.kind} {tok.match!r}", tok.start, tok.end)
