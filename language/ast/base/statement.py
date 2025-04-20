from dataclasses import dataclass


@dataclass
class Statement:
    """
    Base class for all statements.
    """

    def __str__(self):
        return "STATEMENT"
