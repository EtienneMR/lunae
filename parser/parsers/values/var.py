from parser.parsers.functions.funccall import parse_func_call
from parser.reader import ParserReader

from language.ast.values.var import Var
from tokenizer.grammar import TokenKind


def parse_var(reader: ParserReader):
    name = reader.expect(TokenKind.IDENT).match

    if reader.is_followed(TokenKind.LPAREN):
        return parse_func_call(reader, name)
    return Var(name)
