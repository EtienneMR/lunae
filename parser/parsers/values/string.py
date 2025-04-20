from parser.reader import ParserReader

from language.ast.values.string import String
from tokenizer.grammar import TokenKind


def parse_string(reader: ParserReader):
    token = reader.expect(TokenKind.STRING)
    return String(token.value)
