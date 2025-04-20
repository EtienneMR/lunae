from parser.reader import ParserReader

from language.ast.values.number import Number
from tokenizer.grammar import TokenKind


def parse_number(reader: ParserReader) -> Number:
    token = reader.expect(TokenKind.NUMBER)
    return Number(token.value)
