"""
This module provides utility functions for string manipulation.
"""

INDENT = "  "


def indent(obj, indent=INDENT) -> str:
    """
    Indent each line of the str(obj) for pretty printing.

    Args:
        obj (Any): The object to convert to a string and indent.
        indent (str): The string to use for indentation.

    Returns:
        str: The indented string.
    """
    return "\n".join(f"{indent}{l}" for l in str(obj).split("\n"))
