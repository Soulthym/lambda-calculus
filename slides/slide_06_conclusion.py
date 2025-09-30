from lc.lc import *

# Let's recall all definitions

TRUE = lambda a: lambda b: a
FALSE = lambda a: lambda b: b
ZERO = lambda f: lambda x: x
SUCC = lambda n: (lambda f: lambda x: f(n(f)(x)))
ONE = SUCC(ZERO)
TWO = SUCC(ONE)
THREE = SUCC(TWO)
FOUR = SUCC(THREE)
FIVE = SUCC(FOUR)
PAIR = lambda a: lambda b: lambda f: f(a)(b)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)
PREV = lambda p: PAIR(SUCC(FIRST(p)))(FIRST(p))
START = PAIR(ZERO)(ZERO)
PRED = lambda n: SECOND(n(PREV)(START))
SUB = lambda a: lambda b: b(PRED)(a)
def TRUE_LAZY(a):
    return lambda b: a()
def FALSE_LAZY(a):
    return lambda b: b()
IS_ZERO = lambda n: n(lambda f: FALSE_LAZY)(TRUE_LAZY)
MUL = lambda a: lambda b: (lambda f: b(a(f)))
Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))

FACT = Z(lambda f: lambda n: \
        IS_ZERO(n)\
        (lambda: ONE)\
        (lambda: MUL(n)(f(PRED(n)))))
inc = lambda x: x + 1
print(f"{FACT(FIVE)(inc)(0) = }")  # 120
assert FACT(FIVE)(inc)(0) == 120

# We did it!
banner("Conclusion", char="=")
# We have implemented:
# - Boolean logic (TRUE, FALSE, IF)
# - Natural numbers (ZERO, SUCC, ADD, MUL, PRED, SUB)
# - Recursion (Y, Z)
# - Factorial (FACT)
print()
# All using only functions!
# This shows the power of lambda calculus as a foundation for logic,
# shows how functional programming works under the hood,
# and gives insights into the design of programming languages.

# Rules
banner("Notes on the Lambda Calculus", char="=")
# 1. Everything is a function.
# 2. Functions take exactly one argument.
# 3. Functions return exactly one value
# 4. Functions are anonymous.
# 5. There is no statement, only expressions.
# Everything is computed by rewriting expressions,
# We say its a rewriting system.

# Computations happen with one of these rules:
# - Beta reduction: (λx.x)(y) → y
# - Alpha conversion: λx.x → λy.y
# - Eta expansion: f → λx.f(x)
# No name collisions are allowed.

# Some evaluation strategies allow for 'beta-optimality'
# meaning that the number of beta reductions is minimal in all cases.
# This is not the case in Python, or even haskell.
# This language is confluent:
# the order of evaluation does not change the result (if lazy).
# Next time we will explore what such a beta-optimal runtime for (a slight variation of) the lambda calculus could look like!
# It is called interaction nets, and can be trivially parallelized.
# This could have applications around speeding up FFTs, and program search (for proof assistants), where some programs exhibit negative complexity on massivwly shared computations.

banner("The End", char="=")
# Thank you for your attention!
# by Thybault, 2025

# Citations

# In great part, this was inspired by:
# David Beazley's talk 'Lambda calculus from the ground up': https://m.youtube.com/watch?v=pkCLMl0e_0k


# Other resources:
# 2swap's video 'What is PLUS times PLUS': https://www.youtube.com/watch?v=RcVA8Nj6HEo
# The ruliology of lambda by Stephen Wolfram: https://writings.stephenwolfram.com/2025/09/the-ruliology-of-lambdas/
# a beta optimal lambda calculus interpreter: https://github.com/etiams/optiscope
# HigherOrderCo: working on program search for proof assistants: https://github.com/HigherOrderCO
