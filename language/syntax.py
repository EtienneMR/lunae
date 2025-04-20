"""
This module defines the syntax rules for the language.
It includes keywords, binary operators, and unary operators.
"""

from dataclasses import dataclass


@dataclass
class Operator:
    operator: str
    priority: int
    function: str

    @staticmethod
    def dict(operators: list[tuple[str, int, str]]):
        return {op[0]: Operator(*op) for op in operators}


KEYWORDS = {"if", "else", "for", "in", "while", "func"}
BINARY_OPERATORS = Operator.dict(
    [
        ("+", 1, "add"),
        ("-", 1, "sub"),
        ("*", 2, "mul"),
        ("/", 2, "div"),
        ("%", 2, "mod"),
        ("==", 0, "is"),
        (">", 0, "more"),
        ("<", 0, "less"),
    ]
)
UNARY_OPERATORS = Operator.dict(
    [
        ("-", 0, "neg"),
        ("!", 0, "not"),
    ]
)
