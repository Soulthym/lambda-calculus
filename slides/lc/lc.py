from __future__ import annotations
from functools import wraps
from ast import dump as ast_dump, iter_fields, parse
import ast
_Unparser = getattr(ast, "_Unparser")
from inspect import getsource
from textwrap import dedent
from pprint import pp
from typing import cast
from .scope import Scope
from .pretty import Pretty

def dump(node):
    return ast_dump(node, indent=4)

def banner(msg, char="=", width=60):
    sz = len(msg) + 2
    if sz >= width:
        print(char * width)
        print(msg)
        print(char * width)
        return
    diff = width - sz
    l = diff // 2
    r = diff - l
    print(char * l, msg, char * r)

def pretty(printer, obj, stream, indent, allowance, context, level):
    cls_name = obj.__class__.__name__
    indent += len(cls_name) + 1
    keys = getattr(obj, "_pretty_fields", None)
    items = [(k, getattr(obj, k)) for k in keys] if keys else []
    stream.write(cls_name + '(')
    printer._format_namespace_items(items, stream, indent, allowance, context, level)
    stream.write(')')

class Var(ast.expr, metaclass=Pretty):
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

class Lam(ast.expr, metaclass=Pretty):
    _fields = ("var", "body")
    _pretty_fields = _fields
    def __init__(self, var: Var, body: ast.expr):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"Lam(var={self.var!r}, body={self.body!r})"

    def __str__(self):
        return unparse(self)

    @staticmethod
    def __pretty__(printer, self, stream, indent, allowance, context, level):
        pretty(printer, self, stream, indent, allowance, context, level)


class App(ast.expr, metaclass=Pretty):
    _fields = ("func", "arg")
    _pretty_fields = _fields
    def __init__(self, func: ast.expr, arg: ast.expr):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"App(func={self.func!r}, arg={self.arg!r})"

    def __str__(self):
        return unparse(self)

    @staticmethod
    def __pretty__(printer, self, stream, indent, allowance, context, level):
        pretty(printer, self, stream, indent, allowance, context, level)

class Term(ast.Expression, metaclass=Pretty):
    _pretty_fields = ("body",)

    def __repr__(self):
        return repr(self.body)

    def __str__(self):
        return str(self.body)

    @staticmethod
    def __pretty__(printer, self, stream, indent, allowance, context, level):
        pretty(printer, self, stream, indent, allowance, context, level)

    def compile(self):
        code = compile(self, "<lc>", mode="eval")
        return code

class CreateLambdaTerm(ast.NodeVisitor):
    term: ast.expr
    vars: Scope[str, Var]
    max_var: int
    first: bool
    ast: ast.AST
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
        self.term = node # type: ignore
        return super().visit(node)

    def new_var(self) -> Var:
        var = Var(self.max_var)
        self.max_var += 1
        return var

    def visit_Lambda(self, node: ast.Lambda):
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
        body: ast.expr = self.term  # type: ignore
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
        func: ast.expr = self.term  # type: ignore
        for arg in node.args:
            # print(f"arg: {dump(arg)}")
            self.visit(arg)
            arg: ast.expr = self.term  # type: ignore
            func = App(func, arg)
        self.term = func

    def result(self) -> Term:
        ast.fix_missing_locations(self.term)
        return Term(body=self.term)

def lc(f) -> Term:
    """Convert a Python lambda function to a lambda calculus term."""
    src = dedent(getsource(f))
    tree = parse(src)
    visitor = CreateLambdaTerm()
    visitor.visit(tree)
    # print(visitor.term)
    # print(visitor.vars)
    return visitor.result()

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

def unparse(term: ast.AST) -> str:
    unparser = Unparser()
    return unparser.visit(term)

class LambdaToAst(ast.NodeVisitor):
    ast: ast.AST
    first: bool
    def __init__(self):
        self.ast = None  # type: ignore
        self.first = True

    def visit(self, node: ast.AST):
        if self.first:
            self.first = False
            self.ast = node
        return super().visit(node)

    def update_parent(self, parent: ast.AST, child: ast.AST, field: str, index: int | None = None):
        if field is not None:
            if index is not None:
                getattr(parent, field)[index] = child
            else:
                setattr(parent, field, child)

    def generic_visit(self, node):
        # print(f"generic_visit({unparse(node)})")
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, ast.AST):
                        new = self.visit(item)
                        if new is not None:
                            # if we updated the child, update the parent
                            # and only visit the new node
                            self.update_parent(node, new, field=field, index=index)
                            return self.generic_visit(new)
            elif isinstance(value, ast.AST):
                new = self.visit(value)
                if new is not None:
                    # if we updated the child, update the parent
                    # and only visit the new node
                    self.update_parent(node, new, field=field)
                    return self.generic_visit(new)


    def visit_Var(self, node: Var):
        # print(f"visit_Var({node})")
        new = ast.Name(id=node.name, ctx=ast.Load())
        self.generic_visit(new)
        return new

    def visit_Lam(self, node: Lam):
        # print(f"visit_Lam({node})")
        new = ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=node.var.name)],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=node.body,
        )
        self.generic_visit(new)
        return new

    def visit_App(self, node: App):
        # print(f"visit_App({node})")
        new = ast.Call(
            func=node.func,
            args=[node.arg],
            keywords=[],
        )
        self.generic_visit(new)
        return new

    def result(self) -> ast.Expression:
        expr = cast(ast.Expression, self.ast)
        ast.fix_missing_locations(expr)
        return ast.Expression(body=expr.body)


def lc_to_ast(term: ast.AST) -> ast.Expression:
    visitor = LambdaToAst()
    visitor.visit(term)
    res = visitor.result()
    return res

_compile = compile
@wraps(_compile)
def compile(obj, *args, **kwargs):
    if isinstance(obj, ast.AST):
        obj = lc_to_ast(obj)
    return _compile(obj, *args, **kwargs)

def plc(f, title=""):
    """Pretty-print a lambda calculus term from a Python lambda function."""
    if title:
        print(title, end=" = ")
    print(lc(f))

def assert_lc(f, expected: str):
    term = str(lc(f))
    print(f"term: {term}")
    assert term == expected, f"Expected: {expected!r}, got: {term!r}"

def test_front():
    print("Testing lc...")
    a = lambda x: x
    assert_lc(a, "λx0.(x0)")
    b = lambda x: lambda y: x
    assert_lc(b, "λx0.(λx1.(x0))")
    c = lambda x: lambda y: y
    assert_lc(c, "λx0.(λx1.(x1))")
    d = lambda x: lambda y: x(y)
    assert_lc(d, "λx0.(λx1.(x0(x1)))")
    e = lambda f: lambda x: f(d(x))
    assert_lc(e, "λx0.(λx1.(x0(d(x1))))")
    f = lambda x, y: x(y)
    assert_lc(f, "λx0.(λx1.(x0(x1)))")
    g = lambda x, y, z: x(y, z)
    assert_lc(g, "λx0.(λx1.(λx2.(x0(x1)(x2))))")
    print("Testing compilation...")
    h = lambda x, y, z: x(y, z)
    term = lc(h)
    print(f"term: {term}")
    pp(term)
    tree = lc_to_ast(term)
    print(f"tree: {dump(tree)}")

def compare_ast(term: ast.AST, expected: str):
    tree = lc_to_ast(term)
    src = unparse(tree)
    print(f"src: {src}")
    assert src == expected, f"Expected: {expected!r}, got: {src!r}"

def test_back():
    print("Testing back conversion from LC to Python AST...")
    g = lambda x, y, z: x(y, z)
    term = lc(g)
    compare_ast(term, "lambda x0: lambda x1: lambda x2: x0(x1)(x2)")

if __name__ == "__main__":
    test_front()
    test_back()
    print("All tests passed.")
