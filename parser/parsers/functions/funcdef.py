from parser.parsers.base.block import parse_block
from parser.reader import ParserReader

from language.ast.functions.funcdef import FuncDef
from tokenizer.grammar import TokenKind


def parse_func_def(reader: ParserReader):
    reader.expect(TokenKind.KEYWORD, "func")
    name = reader.expect(TokenKind.IDENT).match
    reader.expect(TokenKind.LPAREN)
    params: list[str] = []
    if not reader.match(TokenKind.RPAREN):
        while True:
            params.append(reader.expect(TokenKind.IDENT).match)
            if reader.match(TokenKind.RPAREN):
                break
            reader.expect(TokenKind.COMMA)

    reader.expect(TokenKind.COLON)
    return FuncDef(name, params, parse_block(reader))
