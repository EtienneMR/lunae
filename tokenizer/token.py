"""
This module defines the Token class and related utilities for tokenization.
"""

from dataclasses import dataclass

from tokenizer.grammar import TokenKind
from utils.errors import TokenizerError
from utils.SourcePosition import SourcePosition


@dataclass
class Token:
    """
    Represents a token in the source code.

    Attributes:
        kind (str): The type of the token (e.g., "NUMBER", "STRING").
        match (str): The matched string for the token.
        start (SourcePosition): The starting position of the token.
        end (SourcePosition): The ending position of the token.
    """

    kind: TokenKind
    match: str
    start: SourcePosition
    end: SourcePosition

    @property
    def value(self) -> str | float:
        """
        Returns the value of the token based on its kind.

        Returns:
            str | float: The value of the token.

        Raises:
            TokenizerError: If the token kind is unexpected.
        """
        if self.kind == TokenKind.STRING:
            return bytes(self.match[1:-1], "utf-8").decode("unicode_escape")
        if self.kind == TokenKind.NUMBER:
            return float(self.match)

        err = TokenizerError(
            f"Unexpected token kind: {self.kind} has no value", self.start, self.end
        )
        err.add_note(f"Match: {self.match!r}")
        raise err
