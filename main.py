"""
This module serves as the entry point for the plang package.
It initializes the tokenizer and parser to process the source code.
"""

from parser import parse

from interpreter.interpreter import Interpreter
from tokenizer import tokenize
from utils.errors import SourceError

if __name__ == "__main__":
    SOURCE = """
while (b<10):
    if a: print(b)
"""
    try:
        tokens = tokenize(SOURCE)
        ast = parse(tokens)
        print(ast)
        print(Interpreter().eval(ast))

    except SourceError as e:
        e.with_source(SOURCE)
        raise e
