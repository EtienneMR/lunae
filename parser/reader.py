from typing import Optional

from tokenizer.grammar import TokenKind
from tokenizer.token import Token
from utils.errors import ParserError


class ParserReader:
    """
    A utility class for reading and processing tokens during parsing.

    Attributes:
        tokens (list[Token]): The list of tokens to process.
        pos (int): The current position in the token list.
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def skip(self):
        self.pos += 1

    def peek(self, offset: int = 0) -> Optional[Token]:
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def is_followed(self, kind: TokenKind, match: str | None = None, offset: int = 0):
        peek = self.peek(offset)
        return peek and peek.kind == kind and (match is None or peek.match == match)

    def match(self, kind: TokenKind, value: str | None = None) -> Optional[Token]:
        tok = self.peek()
        if tok and tok.kind == kind and (value is None or tok.match == value):
            self.skip()
            return tok
        return None

    def expect(self, kind: TokenKind, match: str | None = None) -> Token:
        tok = self.match(kind, match)
        if not tok:
            expected = match or kind
            actual = self.peek()
            raise ParserError(
                f"Expected '{expected}', got '{actual.kind if actual else None}'",
                actual.start if actual else None,
                actual.end if actual else None,
            )
        return tok
