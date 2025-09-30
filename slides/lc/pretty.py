import sys
from functools import wraps
from pprint import PrettyPrinter

def register_pretty(cls, pretty, convert=None):
    if isinstance(cls, type):
        __repr__ = cls.__repr__
    else:
        __repr__ = cls
    assert callable(__repr__)
    if isinstance(pretty, type):
        pretty = pretty.__pretty__
    assert callable(pretty)
    PrettyPrinter._dispatch[__repr__] = pretty  # type: ignore
    if convert:
        _repr = sys.modules['builtins'].repr

        @wraps(_repr)
        def repr(obj):
            if isinstance(obj, cls):
                obj = convert(obj)
            return _repr(obj)
        setattr(sys.modules['builtins'], 'repr', repr)

class Pretty(type):
    def __new__(cls, name, bases, scope, **kw):
        subcls = super().__new__(cls, name, bases, scope, **kw)
        if "__pretty__" in scope:
            if "__repr__" not in scope:
                raise AttributeError(
                    "%s defines __pretty__ but not __repr__"
                    % name)
            register_pretty(scope["__repr__"], scope["__pretty__"])
        return subcls

    def __repr__(cls):
        return cls.__name__
