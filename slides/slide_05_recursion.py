from lc.lc import *
from slide_02_numbers import *
from slide_03_substraction import *
from slide_04_laziness import *

# Let's recall FACT

def TRUE(a):
    return lambda b: a()
def FALSE(a):
    return lambda b: b()
IS_ZERO = lambda n: n(lambda f: FALSE)(TRUE)
FACT = lambda n: \
        IS_ZERO(n)\
        (lambda: ONE)\
        (lambda: MUL(n)(FACT(PRED(n))))

# Notice how FACT calls itself?
# This is called recursion, and is not allowed in pure lambda calculus
# We will see how to implement recursion now
banner("Recursion", char="*")

# The idea is to create a function that takes another function as argument, and applies it to its own result
# We'll call it Y
Y = lambda f: (lambda x: f(x(x)))(lambda x: f(x(x)))
# For the same reason as before, we need to wrap the argument of f in a lambda to avoid eager evaluation
Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))

# Let's now define FACT using Z
FACT = Z(lambda f: lambda n: \
        IS_ZERO(n)\
        (lambda: ONE)\
        (lambda: MUL(n)(f(PRED(n)))))

# Let's test FACT
print(f"{FACT(FIVE)(inc)(0) = }")  # 120
assert FACT(FIVE)(inc)(0) == 120
print(f"{FACT(THREE)(inc)(0) = }")  # 6
assert FACT(THREE)(inc)(0) == 6

# It works!
