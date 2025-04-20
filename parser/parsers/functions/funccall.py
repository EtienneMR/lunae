from parser.parsers.base.expr import parse_expr
from parser.reader import ParserReader

from language.ast.base.expr import Expr
from language.ast.functions.funccall import FuncCall
from tokenizer.grammar import TokenKind


def parse_func_call(reader: ParserReader, name: str):
    reader.expect(TokenKind.LPAREN)

    args: list[Expr] = []

    if not reader.match(TokenKind.RPAREN):
        while True:
            args.append(parse_expr(reader))
            if reader.match(TokenKind.RPAREN):
                break
            reader.expect(TokenKind.COMMA)

    return FuncCall(name, args)
