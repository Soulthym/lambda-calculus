from __future__ import annotations
from ast import dump as ast_dump, parse, NodeVisitor, AST, _Unparser
from inspect import getsource
from textwrap import dedent
from types import CodeType
from pprint import pp
from scope import Scope
from pretty import Pretty

def dump(node):
    return ast_dump(node, indent=4)

def pretty(printer, obj, stream, indent, allowance, context, level):
    cls_name = obj.__class__.__name__
    indent += len(cls_name) + 1
    keys = getattr(obj, "_pretty_fields", None)
    items = [(k, getattr(obj, k)) for k in keys] if keys else []
    stream.write(cls_name + '(')
    printer._format_namespace_items(items, stream, indent, allowance, context, level)
    stream.write(')')

class Var(metaclass=Pretty):
    _pretty_fields = ("name",)
    def __init__(self, id: int):
        self.id = id
        name = f"x{self.id}"
        self.name = name

    def __repr__(self):
        return f"Var(name={self.name!r})"

    def __str__(self):
        return self.name

    @staticmethod
    def __pretty__(printer, self, stream, indent, allowance, context, level):
        pretty(printer, self, stream, indent, allowance, context, level)

class Lam(metaclass=Pretty):
    _fields = ("var", "body")
    _pretty_fields = _fields
    def __init__(self, var: Var, body: Term):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"Lam(var={self.var!r}, body={self.body!r})"

    def __str__(self):
        return unparse(self)

    @staticmethod
    def __pretty__(printer, self, stream, indent, allowance, context, level):
        pretty(printer, self, stream, indent, allowance, context, level)


class App(metaclass=Pretty):
    _fields = ("func", "arg")
    _pretty_fields = _fields
    def __init__(self, func: Term, arg: Term):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"App(func={self.func!r}, arg={self.arg!r})"

    def __str__(self):
        return unparse(self)

    @staticmethod
    def __pretty__(printer, self, stream, indent, allowance, context, level):
        pretty(printer, self, stream, indent, allowance, context, level)

type Term = Lam | App | Var | AST

class CreateLambdaTerm(NodeVisitor):
    term: Term
    vars: Scope[str, Var]
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
        # print(f"visit({dump(node)})")
        if self.first:
            # print("=" * 40)
            # print(f"visit({dump(node)})")
            # print("=" * 40)
            self.first = False
            self.ast = node
        self.term = node
        return super().visit(node)

    def new_var(self) -> Var:
        var = Var(self.max_var)
        self.max_var += 1
        return var

    def visit_Lambda(self, node):
        # print(f"visit_Lambda({dump(node)})")
        self.vars.enter()
        params = []
        for arg in node.args.args:
            # print(f"arg: {dump(arg)}")
            var_name = arg.arg
            var = self.new_var()
            self.vars[var_name] = var
            params.append(var)
        self.generic_visit(node)
        body = self.term
        for var in reversed(params):
            body = Lam(var, body)
        self.term = body
        self.vars.exit()

    def visit_Name(self, node):
        # print(f"visit_Name({dump(node)})")
        if node.id in self.vars:
            var = self.vars[node.id]
            self.term = var
            self.vars[node.id] = var

    def visit_Call(self, node):
        # print(f"visit_Call({dump(node)})")
        self.visit(node.func)
        func = self.term
        for arg in node.args:
            # print(f"arg: {dump(arg)}")
            self.visit(arg)
            func = App(func, self.term)
        self.term = func

def lc(f) -> Term:
    """Convert a Python lambda function to a lambda calculus term."""
    src = dedent(getsource(f))
    ast = parse(src, mode="exec")
    visitor = CreateLambdaTerm()
    visitor.visit(ast)
    # print(visitor.term)
    # print(visitor.vars)
    return visitor.term

class Unparser(_Unparser):
    def traverse(self, node):
        if isinstance(node, (Lam, App, Var)):
            method = "visit_" + node.__class__.__name__
            visit = getattr(self, method)
            visit(node)
            return "".join(self._source)
        return super().traverse(node)

    def visit_Lam(self, node):
        self.write("λ")
        self.traverse(node.var)
        self.write(".(")
        self.traverse(node.body)
        self.write(")")

    def visit_App(self, node):
        self.traverse(node.func)
        self.write("(")
        self.traverse(node.arg)
        self.write(")")

    def visit_Var(self, node):
        self.write(str(node))

def unparse(term: Term) -> str:
    unparser = Unparser()
    return unparser.visit(term)

class LambdaToAst(NodeVisitor):
    parent: AST
    def __init__(self):
        self.parent = None  # type: ignore

    def visit(self, node: Term):
        print(f"visit({dump(node)}, parent={dump(self.parent) if self.parent else None})")
        if isinstance(node, Var):
            self.visit_Var(node)
        elif isinstance(node, Lam):
            self.visit_Lam(node)
        elif isinstance(node, App):
            self.visit_App(node)
        else:
            self.parent = node
            super().visit(node)


    def visit_Var(self, node: Var):
        ...

    def visit_Lam(self, node: Lam):
        ...

    def visit_App(self, node: App):
        ...

def lc_to_ast(term: Term) -> AST:
    visitor = LambdaToAst()
    visitor.visit(term)
    return visitor.parent

def plc(f):
    """Pretty-print a lambda calculus term from a Python lambda function."""
    print(lc(f))

def assert_lc(f, expected: str):
    term = str(lc(f))
    print(f"term: {term}")
    assert term == expected, f"Expected: {expected!r}, got: {term!r}"

if __name__ == "__main__":
    print("Testing lc...")
    l = lambda x: x
    assert_lc(l, "λx0.(x0)")
    l = lambda x: lambda y: x
    assert_lc(l, "λx0.(λx1.(x0))")
    l = lambda x: lambda y: y
    assert_lc(l, "λx0.(λx1.(x1))")
    l = lambda x: lambda y: x(y)
    assert_lc(l, "λx0.(λx1.(x0(x1)))")
    t = lambda f: lambda x: f(l(x))
    assert_lc(t, "λx0.(λx1.(x0(l(x1))))")
    l = lambda x, y: x(y)
    assert_lc(l, "λx0.(λx1.(x0(x1)))")
    l = lambda x, y, z: x(y, z)
    assert_lc(l, "λx0.(λx1.(λx2.(x0(x1)(x2))))")
    print("Testing compilation...")
    l = lambda x, y, z: x(y, z)
    term = lc(l)
    print(f"term: {term}")
    pp(term)
    ast = lc_to_ast(term)
    print(f"ast: {dump(ast)}")
    print("All tests passed.")
