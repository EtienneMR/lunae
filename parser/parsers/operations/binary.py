from parser.parsers.operations.unary import parse_unary
from parser.reader import ParserReader

from language.ast.functions.funccall import FuncCall
from language.syntax import BINARY_OPERATORS
from tokenizer.grammar import TokenKind


def parse_binary(reader: ParserReader, min_prec: int = 0):
    left = parse_unary(reader)
    while True:
        tok = reader.peek()
        if not tok or tok.kind != TokenKind.OP:
            break
        op = BINARY_OPERATORS[tok.match]
        if op.priority < min_prec:
            break
        reader.skip()
        right = parse_binary(reader, min_prec + 1)
        left = FuncCall(op.function, [left, right])
    return left
