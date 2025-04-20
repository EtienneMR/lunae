from parser.parsers.base.expr import parse_expr
from parser.reader import ParserReader

from language.ast.values.assign import Assign
from tokenizer.grammar import TokenKind


def parse_assign(reader: ParserReader):
    name = reader.expect(TokenKind.IDENT).match
    reader.expect(TokenKind.ASSIGN)
    value = parse_expr(reader)
    return Assign(name, value)
