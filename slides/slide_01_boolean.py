from lc.lc import *
from slide_00_intro import *
# What is an if statement?
# It is fundamentally a choice between two alternatives:
# if condition is true: true_case
# if condition is false: false_case
# Kind of like... a physical switch, a transistor!
# Let's start with boolean values

banner("Booleans")
def TRUE(true_case, false_case):
    return true_case
def FALSE(true_case, false_case):
    return false_case
# Notice how TRUE and FALSE *select* between two alternatives
# Now, assuming TRUE and FALSE as defined above, we can rewrite if_ as
banner("currying", char="*")
def if_(condition, true_case, false_case):
    return condition(true_case, false_case)
# Can we go further?
# What is a multiple argument function?
# You can think of the 2 following as equivalent:
def f(x, y):
    return x + y
print(f"{f(2, 3) = }") # 5

def f_cur(x):
    def f_x(y):
        return x + y
    return f_x
print(f"{f_cur(2)(3) = }") # 5
# We call this process currying, after Haskell Curry
# Notice how f_cur takes only one argument, but twice?
# This means we can partially apply functions, only providing some arguments as they come (although in order)
# Notably this allows us to start computing before we have all the arguments

# From now on, we will only use curried functions
# Let's rewrite TRUE
def TRUE_cur(true_case):
    def TRUE_true_case(false_case):
        return true_case
    return TRUE_true_case

# This is getting tedious, so let's use lambda notation
# A lambda expression is just a function without a name
# We will keep the outer function name for debugging purposes# but keep in mind that we could apply this transformation to any function
def TRUE(a):
    return lambda b: a
def FALSE(a):
    return lambda b: b
def if_(cond):
    return lambda a: lambda b: cond(a)(b)
def fact(n): # do not run this yet
    return if_(n == 0)(1)(n * fact(n - 1))

# What can we do with booleans?
# We can define logical operations
# NOT:
# a | NOT a
# 0 | 1
# 1 | 0
banner("NOT")
def _NOT(a):
    return ... # Fill this in

def _NOT(a):
    return a # we only have a, so lets return it for now
def _NOT(a):
    return a(...) # We know that a is a function
def _NOT(a):
    return a(...)(...) # We know that a takes two arguments,
                       # and that a acts as an if statement/
def _NOT(a):
    return a(FALSE)(...) # If a is TRUE, we want to return FALSE
def _NOT(a):
    return a(FALSE)(TRUE) # If a is FALSE, we want to return TRUE
# Let's make it a lambda
NOT = lambda a: a(FALSE)(TRUE)
plc(NOT, "NOT")
# Let's test our code
plc(NOT(FALSE), "NOT(FALSE)")
plc(NOT(TRUE), "NOT(TRUE)")
assert NOT(FALSE) == TRUE
assert NOT(TRUE) == FALSE

# AND:
# a | b | a AND b
# 0 | 0 | 0
# 0 | 1 | 0
# 1 | 0 | 0
# 1 | 1 | 1
banner("AND")
def _AND(a):
    return lambda b: ... # Fill this in
# Notice how the result is true only if both a and b are true# This means that when a is true, the result is b
# and when a is false, the result is false, which is just a
AND = lambda a: lambda b: a(b)(a)
plc(AND, "AND")
# Let's test our code
plc(AND(FALSE)(FALSE), "AND(FALSE, FALSE)")
plc(AND(FALSE)(TRUE), "AND(FALSE, TRUE)")
plc(AND(TRUE)(FALSE), "AND(TRUE, FALSE)")
plc(AND(TRUE)(TRUE), "AND(TRUE, TRUE)")
assert AND(FALSE)(FALSE) == FALSE
assert AND(FALSE)(TRUE) == FALSE
assert AND(TRUE)(FALSE) == FALSE
assert AND(TRUE)(TRUE) == TRUE

# OR:
# a | b | a OR b
# 0 | 0 | 0
# 0 | 1 | 1
# 1 | 0 | 1
# 1 | 1 | 1
banner("OR")
def _OR(a):
    return lambda b: ... # Fill this in
# Notice how the result is false only if both a and b are false
# This means that:
# when a is true, the result is true, which is just a
# and when a is false, the result is b
OR = lambda a: lambda b: a(a)(b)
plc(OR, "OR")
# Let's test our code
plc(OR(FALSE)(FALSE), "OR(FALSE, FALSE)")
plc(OR(FALSE)(TRUE), "OR(FALSE, TRUE)")
plc(OR(TRUE)(FALSE), "OR(TRUE, FALSE)")
plc(OR(TRUE)(TRUE), "OR(TRUE, TRUE)")
assert OR(FALSE)(FALSE) == FALSE
assert OR(FALSE)(TRUE) == TRUE
assert OR(TRUE)(FALSE) == TRUE
assert OR(TRUE)(TRUE) == TRUE
# We can also define XOR, NAND, NOR, etc.
# but we will leave that as an exercise to the reader
XOR = lambda a: lambda b: ... # Fill this in
NAND = lambda a: lambda b: ... # Fill this in
NOR = lambda a: lambda b: ... # Fill this in
... # Fill this in
