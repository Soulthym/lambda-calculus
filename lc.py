from __future__ import annotations
from ast import dump as ast_dump, parse, NodeVisitor, AST
from inspect import getsource
from textwrap import dedent
from scope import Scope

def dump(node):
    return ast_dump(node, indent=4)

class Var:
    def __init__(self, id: int):
        self.id = id
        name = f"x{self.id}"
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.id

class Name:
    def __init__(self, id: str):
        self.id = id

    def __repr__(self):
        return self.id

class Lam:
    def __init__(self, var: Var, body: Term):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"λ{self.var}.({self.body})"

class App:
    def __init__(self, func: Term, arg: Term):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"{self.func}({self.arg})"

type Ident = Name | Var
type Term = Lam | App | Ident

class LambdaVisitor(NodeVisitor):
    term: Term
    vars: Scope[str, Ident]
    max_var: int
    first: bool
    ast: AST
    def __init__(self, vars=None):
        self.term = None  # type: ignore
        self.vars = vars or Scope()
        self.max_var = 0
        self.first = True
        self.ast = None  # type: ignore

    def visit(self, node):
        if self.first:
            # print("=" * 40)
            # print(f"visit({dump(node)})")
            # print("=" * 40)
            self.first = False
            self.ast = node
        return super().visit(node)

    def new_var(self) -> Var:
        var = Var(self.max_var)
        self.max_var += 1
        return var

    def visit_Lambda(self, node):
        # print(f"visit_Lambda({dump(node)})")
        var_name = node.args.args[0].arg
        var = self.new_var()
        self.vars.enter()
        self.vars[var_name] = var
        self.generic_visit(node)
        body = self.term
        self.term = Lam(var, body)
        self.vars.exit()

    def visit_Name(self, node):
        # print(f"visit_Name({dump(node)})")
        if node.id in self.vars:
            var = self.vars[node.id]
            self.term = var
            self.vars[node.id] = var
        else:
            name = Name(node.id)
            self.term = name
            self.vars[node.id] = name

    def visit_Call(self, node):
        # print(f"visit_Call({dump(node)})")
        self.visit(node.func)
        func = self.term
        self.visit(node.args[0])
        arg = self.term
        self.term = App(func, arg)

def lam(f) -> Term:
    """Convert a Python lambda function to a lambda calculus term."""
    src = dedent(getsource(f))
    ast = parse(src)
    visitor = LambdaVisitor()
    visitor.visit(ast)
    # print(visitor.vars)
    return visitor.term

def assert_lam(f, expected: str):
    term = lam(f)
    r = repr(term)
    print(r)
    assert r == expected, f"Expected: {expected}, got: {r}"

if __name__ == "__main__":
    l = lambda x: x
    assert_lam(l, "λx0.(x0)")
    l = lambda x: x
    assert_lam(l, "λx0.(x0)")
    l = lambda x: lambda y: x
    assert_lam(l, "λx0.(λx1.(x0))")
    l = lambda x: lambda y: y
    assert_lam(l, "λx0.(λx1.(x1))")
    l = lambda x: lambda y: x(y)
    assert_lam(l, "λx0.(λx1.(x0(x1)))")
    t = lambda f: lambda x: f(l(x))
    assert_lam(t, "λx0.(λx1.(x0(l(x1))))")
    print("All tests passed.")

