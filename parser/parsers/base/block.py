from parser.parsers.base.expr import parse_expr
from parser.parsers.base.statement import parse_statement
from parser.reader import ParserReader

from language.ast.base.block import Block
from language.ast.base.expr import Expr
from language.ast.base.statement import Statement
from tokenizer.grammar import TokenKind


def parse_block(reader: ParserReader) -> Block | Statement:
    if reader.match(TokenKind.NEWLINE) and reader.is_followed(TokenKind.INDENT):
        reader.expect(TokenKind.INDENT)
        statements: list[Statement] = []
        while not reader.match(TokenKind.DEDENT):
            if reader.match(TokenKind.NEWLINE):
                continue
            statements.append(parse_statement(reader))

        # same behavior
        if len(statements) == 1:
            return statements[0]
        return Block(statements)
    # single-line expression
    expr = parse_expr(reader)
    reader.match(TokenKind.NEWLINE)
    return expr


def parse_reader(reader: ParserReader) -> Block:
    statements: list[Statement] = []
    while reader.peek():
        if reader.match(TokenKind.NEWLINE):
            continue
        statements.append(parse_statement(reader))
    return Block(statements)
