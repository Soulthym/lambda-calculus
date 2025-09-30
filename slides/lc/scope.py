from __future__ import annotations
type Env[K, V] = dict[K, V]

def repr_env(env: Env) -> str:
    return ", ".join(f"{k}={v}" for k, v in env.items())

class Root[K, V]:
    env: Env[K, V]
    def __init__(self, env: Env[K, V]):
        self.env = env
    def __repr__(self):
        return f"Root({repr_env(self.env)})"
class Nested[K, V]:
    parent: LexicalScope[K, V]
    env: Env[K, V]
    def __init__(self, parent: LexicalScope[K, V], env: Env[K, V]):
        self.parent = parent
        self.env = env
    def __repr__(self):
        if not self.env:
            return f"Nested({self.parent})"
        return f"Nested({self.parent}, {repr_env(self.env)})"

type LexicalScope[K, V] = Root[K, V] | Nested[K, V]

class Scope[K, V]:
    scope: LexicalScope[K, V]
    def __init__(self):
        self.scope = Root({})

    def __repr__(self):
        return f"Scope.{self.scope}"

    def enter(self):
        # print(f"{self}.enter()")
        if isinstance(self.scope, (Root, Nested)):
            self.scope = Nested(self.scope, {})
        else:
            raise RuntimeError(f"Invalid scope: {self.scope}")

    def exit(self):
        # print(f"{self}.exit()")
        if isinstance(self.scope, Root):
            raise RuntimeError("Cannot exit from root scope")
        elif isinstance(self.scope, Nested):
            self.scope = self.scope.parent
        else:
            raise RuntimeError(f"Invalid scope: {self.scope}")

    def to_dict(self) -> Env[K, V]:
        env = {}
        scope = self.scope
        parents = []
        while isinstance(scope, Nested):
            parents.append(scope)
            scope = scope.parent
        if isinstance(scope, Root):
            parents.append(scope)
        for p in reversed(parents):
            env.update(p.env)
        return env

    def __contains__(self, key: K) -> bool:
        # print(f"{key} in {self}?")
        scope = self.scope
        while True:
            if key in scope.env:
                return True
            if isinstance(scope, Root):
                return False
            else:
                scope = scope.parent

    def __getitem__(self, key: K) -> V:
        # print(f"{self}[{key}]")
        scope = self.scope
        while True:
            if key in scope.env:
                return scope.env[key]
            if isinstance(scope, Root):
                raise KeyError(f"Key not found: {key}")
            else:
                scope = scope.parent

    def __setitem__(self, key: K, value: V):
        # print(f"{self}[{key}] = {value}")
        self.scope.env[key] = value

if __name__ == "__main__":
    s = Scope[str, int]()
    print(s.to_dict())  # {}
    s.enter()
    d = s.to_dict()  # {}
    print(d)
    assert d == {}
    s.scope.env["x"] = 1
    d = s.to_dict()  # {'x': 1}
    print(d)
    assert d == {"x": 1}
    s.enter()
    d = s.to_dict()  # {'x': 1}
    print(d)
    assert d == {"x": 1}
    s.scope.env["y"] = 2
    d = s.to_dict()  # {'x': 1, 'y': 2}
    print(d)
    assert d == {"x": 1, "y": 2}
    s.exit()
    d = s.to_dict()  # {'x': 1}
    print(d)
    assert d == {"x": 1}
    s.enter()
    s.scope.env["x"] = 3
    d = s.to_dict()  # {'x': 3}
    print(d)
    assert d == {"x": 3}
    s.exit()
    d = s.to_dict()  # {'x': 1}
    print(d)
    assert d == {"x": 1}
    s.exit()
    d = s.to_dict()  # {}
    print(d)
    assert d == {}
    print("All tests passed.")
