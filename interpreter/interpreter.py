from parser import parse
from typing import Any

from interpreter.environement import Environment
from language.ast.base.block import Block
from language.ast.base.expr import Expr
from language.ast.controls.forexpr import ForExpr
from language.ast.controls.ifexpr import IfExpr
from language.ast.controls.whileexpr import WhileExpr
from language.ast.functions.funccall import FuncCall
from language.ast.functions.funcdef import FuncDef
from language.ast.values.assign import Assign
from language.ast.values.number import Number
from language.ast.values.string import String
from language.ast.values.var import Var
from tokenizer import tokenize
from utils.errors import InterpreterError

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


def create_global_env() -> Environment:
    env = Environment()

    for op, fn in OPERATORS.items():
        env.set(op, fn)

    return env


class Interpreter:
    """
    The main interpreter class that evaluates the abstract syntax tree (AST).
    """

    def __init__(self):
        """
        Initializes the interpreter with a global environment.
        """
        self.global_env = create_global_env()

    def execute(self, source: str):
        """
        Execute the provided source.
        This method is sugar for interpreter.eval(parser.parse(tokenizer.tokenize(source)))

        Args:
            source (str): The code to be executed.

        Returns:
            Any: The result of the execution
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        return self.eval(ast)

    def eval(self, node: Expr, env: "Environment | None" = None) -> Any:
        """
        Evaluates a given AST node.

        Args:
            node (Expr): The AST node to evaluate.
            env (Environment | None): The environment to use for evaluation.

        Returns:
            Any: The result of the evaluation.

        Raises:
            InterpreterError: If the node type is unknown.
        """
        if env is None:
            env = self.global_env

        method = getattr(self, "eval_" + node.__class__.__name__, None)

        if method is None:
            raise InterpreterError(f"Unknown node to eval: {node}", None)
        else:
            return method(node, env)

    def eval_Number(self, node: Number, env: Environment):
        """
        Evaluates a number node.

        Args:
            node (Number): The number node.
            env (Environment): The current environment.

        Returns:
            int | float: The value of the number.
        """
        return node.value

    def eval_String(self, node: String, env: Environment):
        """
        Evaluates a string node.

        Args:
            node (String): The string node.
            env (Environment): The current environment.

        Returns:
            str: The value of the string.
        """
        return node.value

    def eval_Var(self, node: Var, env: Environment):
        """
        Evaluates a variable node.

        Args:
            node (Var): The variable node.
            env (Environment): The current environment.

        Returns:
            Any: The value of the variable.
        """
        return env.get(node.name)

    def eval_Assign(self, node: Assign, env: Environment):
        """
        Evaluates an assignment node.

        Args:
            node (Assign): The assignment node.
            env (Environment): The current environment.

        Returns:
            Any: The value assigned.
        """
        val = self.eval(node.value, env)
        env.set(node.name, val)
        return val

    def eval_FuncCall(self, node: FuncCall, env: Environment):
        """
        Evaluates a function call node.

        Args:
            node (FuncCall): The function call node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the function call.
        """
        fn = env.get(node.func)
        args = [self.eval(a, env) for a in node.args]
        return fn(*args)

    def eval_IfExpr(self, node: IfExpr, env: Environment):
        """
        Evaluates an if expression node.

        Args:
            node (IfExpr): The if expression node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the evaluation.
        """
        cond = self.eval(node.cond, env)
        return (
            self.eval(node.then_branch, env)
            if cond
            else (self.eval(node.else_branch, env) if node.else_branch else None)
        )

    def eval_WhileExpr(self, node: WhileExpr, env: Environment):
        """
        Evaluates a while expression node.

        Args:
            node (WhileExpr): The while expression node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the evaluation.
        """
        result = None
        while self.eval(node.cond, env):
            result = self.eval(node.body, env)
        return result

    def eval_ForExpr(self, node: ForExpr, env: Environment):
        """
        Evaluates a for expression node.

        Args:
            node (ForExpr): The for expression node.
            env (Environment): The current environment.

        Returns:
            list: The results of evaluating the body for each item in the iterable.
        """
        lst = self.eval(node.iterable, env)
        results = []
        for item in lst:
            env.set(node.var, item)
            results.append(self.eval(node.body, env))
        return results

    def eval_FuncDef(self, node: FuncDef, env: Environment):
        """
        Evaluates a function definition node.

        Args:
            node (FuncDef): The function definition node.
            env (Environment): The current environment.

        Returns:
            Callable: The defined function.
        """

        def function(*args):
            local = Environment(env)
            for name, val in zip(node.params, args):
                local.set(name, val)
            return self.eval(node.body, local)

        env.set(node.name, function)
        return function

    def eval_Block(self, node: Block, env: Environment):
        """
        Evaluates a block node.

        Args:
            node (Block): The block node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the last expr in the block.
        """
        res = None
        for stmt in node.statements:
            res = self.eval(stmt, env)
        return res
