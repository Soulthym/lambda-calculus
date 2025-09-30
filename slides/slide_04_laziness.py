from lc.lc import *
from slide_01_boolean import *
from slide_02_numbers import *
from slide_03_substraction import *
# Let's go back to factorial

banner("Factorial")
def fact(n):
    def if_(condition, true_case, false_case):
        if condition:
            return true_case
        else:
            return false_case
    return if_(
            n == 0,
            1,              # true case
            n * fact(n - 1) # false case
    )
# First, let's make it a lambda
FACT = lambda n: \
        if_(n == 0)\
        (1)\
        (n * FACT(n - 1))
# Then we replace the if_(n == 0) with IS_ZERO
FACT = lambda n: \
        IS_ZERO(n)\
        (1)\
        (n * FACT(n - 1))
# Then we replace 1 with ONE
FACT = lambda n: \
        IS_ZERO(n)\
        (ONE)\
        (n * FACT(n - 1))
# Then we replace n - 1 with PRED(n)
FACT = lambda n: \
        IS_ZERO(n)\
        (ONE)\
        (n * FACT(PRED(n)))
# Finally, we replace n * FACT(PRED(n)) with MUL(n)(FACT(PRED(n)))
FACT = lambda n: \
        IS_ZERO(n)\
        (ONE)\
        (MUL(n)(FACT(PRED(n))))

# There is still a problem here
# We found out earlier that this does not work
# Let's try it again to be sure
# print(f"{FACT(THREE)(inc)(0) = }") # Uncomment this

# This still blows up the stack
# Why?
# Because Python is an eager language, it evaluates function arguments before calling the function
# This means that even if we hit the base case of fact,
# we still need to evaluate n * fact(n - 1) before we can return the result,
# which means we need to evaluate fact(n - 1), and so on... forever

# Let's analyze the if_ function
def if_(cond):
    return lambda a: lambda b: cond(a)(b)
# When we call if_(cond)(a)(b), Python first evaluates a and b, and only then selects one of them
# This means that both a and b are always evaluated, even if we only need one of them
# print(f"{if_(TRUE)(1 * 0)( 1 / 0) = }")  # This breaks even though we only need the first argument
# print(f"{if_(FALSE)(1 / 0)(1 * 0) = }")  # This breaks even though we only need the second argument

# How can we fix this?
# Because we are in python, we need to resort to a trick
# Note that this is not necessary in languages with proper laziness, like Haskell or theorem provers like Rocq or Lean

def TRUE(a):
    return lambda b: a()
#                     ~~
#                     |
# We insert a call here, so that the argument is not evaluated until we actually need it
def FALSE(a):
    return lambda b: b()
def if_(cond):
    return lambda a: lambda b: cond(a)(b)
print(f"{if_(TRUE)(lambda: 1 * 0)(lambda:  1 / 0) = }")
print(f"{if_(FALSE)(lambda: 1 / 0)(lambda: 1 * 0) = }")
assert if_(TRUE)(lambda: 1 * 0)(lambda:  1 / 0) == 0
assert if_(FALSE)(lambda: 1 / 0)(lambda: 1 * 0) == 0
# Hooray, it works!

# Let's fix IS_ZERO
IS_ZERO = lambda n: n(lambda f: FALSE)(TRUE)
# We can now fix FACT
FACT = lambda n: \
        IS_ZERO(n)\
        (lambda: ONE)\
        (lambda: MUL(n)(FACT(PRED(n))))

plc(FACT, "FACT")
ONE_HUNDRED_TWENTY = FACT(FIVE)
print(f"{ONE_HUNDRED_TWENTY(inc)(0) = }")  # 120
assert ONE_HUNDRED_TWENTY(inc)(0) == 120
# It works!
