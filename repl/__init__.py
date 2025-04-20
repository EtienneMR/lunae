"""
This module defines the REPL (Read-Eval-Print Loop) for the language.
"""

import traceback
from parser import parse
from textwrap import dedent

from interpreter.environement import Environment
from interpreter.interpreter import Interpreter
from tokenizer import tokenize
from utils.errors import SourceError
from utils.indent import indent

OPERATORS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
    "mod": lambda a, b: a % b,
    "is": lambda a, b: a == b,
    "less": lambda a, b: a < b,
    "more": lambda a, b: a > b,
    "neg": lambda a: -a,
    "not": lambda a: not a,
}


class REPL:
    """
    Represents the REPL (Read-Eval-Print Loop) for the language.
    """

    def __init__(self):
        """
        Initializes the REPL.
        """
        self.interpreter = Interpreter()
        self.lines = []
        self.DEBUG = False
        self.QUIT = False

        self.reset()

        with open("VERSION") as f:
            VERSION = f.read()

        print(f"LUMA {VERSION} - REPL")
        print('Type "help()" for more information')

    def eval(self, source: str):
        """
        Evaluates a source code string.

        Args:
            source (str): The source code to evaluate.
        """
        try:
            ast = parse(tokenize(source))
            result = None
            for child in ast.statements:
                result = self.interpreter.eval(child)
                formated = indent(result, ". ").replace(". ", "> ", 1)
                print(formated)
        except Exception as e:
            if isinstance(e, SourceError):
                e.with_source(source)

            if self.DEBUG or not isinstance(e, SourceError):
                print(" ERROR ".center(60, "-"))
                traceback.print_exc()
                print("-" * 60)
            else:
                print("ERR", e)
                if e.note:
                    print(e.note)

    def load(self, filename: str):
        """
        Loads and evaluates a source code file.

        Args:
            filename (str): The path to the source code file.
        """
        with open(filename) as f:
            source = f.read()
            try:
                self.eval(source)
            except SourceError as e:
                e.with_source(source)
                raise e

    def debug(self):
        """
        Enables debug mode.
        """
        self.DEBUG = True

    def quit(self):
        """
        Quits the REPL.
        """
        self.QUIT = True

    def print(*args):
        """
        Prints arguments to the console.
        """
        print(" ", *args)

    def help(self, value=None):
        """
        Displays help information for a value or lists available functions and variables.

        Args:
            value (Any, optional): The value to display help for. Defaults to None.
        """
        if value:
            if callable(value):
                target = value
            else:
                target = type(value)

            print("Help on", target.__qualname__)
            if target.__doc__:
                print(indent(dedent(target.__doc__)))
            else:
                print("No information avaiable :-(")
        else:
            functions = []
            others = []
            for name, value in self.interpreter.global_env.vars.items():
                if callable(value):
                    functions.append(f"{name.ljust(15)} - {value.__qualname__}")
                else:
                    others.append(f"{name.ljust(15)} - {repr(value)}")

            print("== FUNCTIONS ==")
            for fn in functions:
                print(fn)
            if others:
                print("== OTHERS ==")
                for val in others:
                    print(val)

    def reset(self):
        """
        Resets the REPL environment.
        """
        env = Environment()

        # REPL
        env.set("load", self.load)
        env.set("quit", self.quit)
        env.set("debug", self.debug)
        env.set("reset", self.reset)
        env.set("help", self.help)

        # DEBUG
        env.set("tokenize", tokenize)
        env.set("parse", parse)

        # BUILT-INS
        env.set("print", self.print)
        env.set("range", lambda n: list(range(int(n))))
        for op, fn in OPERATORS.items():
            env.set(op, fn)

        self.interpreter.global_env = env

    def start(self):
        """
        Starts the REPL loop.
        """
        while not self.QUIT:
            inp = input("... " if self.lines else ">>> ")
            if inp:
                self.lines.append(inp)

            if not inp or (len(self.lines) == 1 and inp[-1] != ":"):
                self.eval("\n".join(self.lines))
                self.lines.clear()
