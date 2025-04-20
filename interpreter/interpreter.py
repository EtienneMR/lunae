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
from utils.errors import InterpreterError


class Interpreter:
    def __init__(self):
        self.global_env = Environment()

    def eval(self, node: Expr, env: "Environment | None" = None) -> Any:
        if env is None:
            env = self.global_env
        method = "eval_" + node.__class__.__name__

        return getattr(self, method)(node, env)

    def eval_Number(self, node: Number, env: Environment):
        return node.value

    def eval_String(self, node: String, env: Environment):
        return node.value

    def eval_Var(self, node: Var, env: Environment):
        return env.get(node.name)

    def eval_Assign(self, node: Assign, env: Environment):
        val = self.eval(node.value, env)
        env.set(node.name, val)
        return val

    def eval_FuncCall(self, node: FuncCall, env: Environment):
        fn = env.get(node.func)
        args = [self.eval(a, env) for a in node.args]
        return fn(*args)

    def eval_IfExpr(self, node: IfExpr, env: Environment):
        cond = self.eval(node.cond, env)
        return (
            self.eval(node.then_branch, env)
            if cond
            else (self.eval(node.else_branch, env) if node.else_branch else None)
        )

    def eval_WhileExpr(self, node: WhileExpr, env: Environment):
        result = None
        while self.eval(node.cond, env):
            result = self.eval(node.body, env)
        return result

    def eval_ForExpr(self, node: ForExpr, env: Environment):
        lst = self.eval(node.iterable, env)
        results = []
        for item in lst:
            env.set(node.var, item)
            results.append(self.eval(node.body, env))
        return results

    def eval_FuncDef(self, node: FuncDef, env: Environment):
        def function(*args):
            local = Environment(env)
            for name, val in zip(node.params, args):
                local.set(name, val)
            return self.eval(node.body, local)

        env.set(node.name, function)
        return function

    def eval_Block(self, node: Block, env: Environment):
        res = None
        for stmt in node.statements:
            res = self.eval(stmt, env)
        return res
