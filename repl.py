import traceback
from parser import parse

from interpreter.environement import Environment
from interpreter.interpreter import Interpreter
from tokenizer import tokenize
from utils.errors import SourceError

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


def REPL():
    with open("VERSION") as f:
        VERSION = f.read()

    print(f"LUMA {VERSION} - REPL")

    interpreter = Interpreter()

    lines = ""

    def reset_env():
        interpreter.global_env = create_env()

    def create_env():
        env = Environment()
        env.set("print", lambda *args: print(*args))
        env.set("range", lambda n: list(range(int(n))))
        env.set("loadFile", load_file)
        env.set("reset", reset_env)
        env.set("QUIT", False)
        env.set("DEBUG", False)
        for op, fn in OPERATORS.items():
            env.set(op, fn)
        return env

    def eval_input(inp: str):
        try:
            ast = parse(tokenize(inp))
            result = None
            for child in ast.statements:
                result = interpreter.eval(child)
                print(">", result)
        except Exception as e:
            if interpreter.global_env.get("DEBUG"):
                print(" ERROR ".center(60, "-"))
                traceback.print_exc()
                print("-" * 60)
            else:
                print("ERR:", e)

    def load_file(filename: str):
        with open(filename) as f:
            source = f.read()
            try:
                eval_input(source)
            except SourceError as e:
                e.with_source(source)
                raise e
        return None

    reset_env()

    while not interpreter.global_env.get("QUIT"):
        inp = input("... " if lines else ">>> ")
        if inp:
            lines += inp + "\n"

        if not inp or (lines == inp + "\n" and inp[-1] != ":"):
            eval_input(lines)
            lines = ""


if __name__ == "__main__":
    REPL()
