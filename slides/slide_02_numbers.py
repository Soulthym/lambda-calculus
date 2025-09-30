from lc.lc import *
# from slide_01_boolean import *
# What is a number?
# It is fundamentally a way to count things
# It is an iterator (Church numerals)

banner("Numbers")
ZERO = ...
ZERO = lambda f: ... # it needs to iterate something
ZERO = lambda f: lambda x: ... # it needs a starting point
ZERO = lambda f: lambda x: x # applies f zero times
ONE = lambda f: lambda x: f(x) # applies f once
TWO = lambda f: lambda x: f(f(x)) # applies f twice
THREE = lambda f: lambda x: f(f(f(x))) # applies f thrice
# Notice how we can define numbers just by describing how many times to apply a function

# Let's test our numbers
# We need a function to apply
def inc(x):
    return x + 1

print(f"{ZERO(inc)(0) = }") # 0
print(f"{ONE(inc)(0) = }")  # 1
print(f"{TWO(inc)(0) = }")  # 2
print(f"{THREE(inc)(0) = }")# 3
assert ZERO(inc)(0) == 0
assert ONE(inc)(0) == 1
assert TWO(inc)(0) == 2
assert THREE(inc)(0) == 3

banner("Church Numerals")
# But this is kind of tedious, can we do better?
# Let's implement peano numbers:
# - there is a zero
# - every number has a successor
# We already have ZERO, let's implement SUCC
SUCC = lambda n: ... # it takes a number n
SUCC = lambda n: (lambda f: lambda x: ...) # it returns a number
SUCC = lambda n: (lambda f: lambda x: f(...)) # it applies f one more time than ...
SUCC = lambda n: (lambda f: lambda x: f(n(...)(...))) # it applies f one more time than n
SUCC = lambda n: (lambda f: lambda x: f(n(f)(x))) # it needs to pass f and x to n

# let's test SUCC
print(f"{SUCC(ZERO)(inc)(0) = }")  # 1
print(f"{SUCC(ONE)(inc)(0) = }")   # 2
print(f"{SUCC(TWO)(inc)(0) = }")   # 3
print(f"{SUCC(THREE)(inc)(0) = }") # 4
assert SUCC(ZERO)(inc)(0) == 1
assert SUCC(ONE)(inc)(0) == 2
assert SUCC(TWO)(inc)(0) == 3
assert SUCC(THREE)(inc)(0) == 4

# We now have more numbers
FOUR = SUCC(THREE)
FIVE = SUCC(FOUR)
print(f"{FOUR(inc)(0) = }")  # 4
print(f"{FIVE(inc)(0) = }")  # 5
assert FOUR(inc)(0) == 4
assert FIVE(inc)(0) == 5

# But we're still missing arithmetic operations
# Let's start with addition

banner("Operations")
banner("Addition", char="*")
ADD = lambda a: lambda b: ... # it takes two numbers a and b
ADD = lambda a: lambda b: a(...)(...) # it needs to apply a times ...
ADD = lambda a: lambda b: a(...)(b) # to b
ADD = lambda a: lambda b: a(SUCC)(b) # it needs to apply SUCC a times to b

# Let's test ADD
print(f"{ADD(THREE)(TWO)(inc)(0) = }")  # 5
print(f"{ADD(FOUR)(FIVE)(inc)(0) = }")  # 9
assert ADD(THREE)(TWO)(inc)(0) == 5
assert ADD(FOUR)(FIVE)(inc)(0) == 9

# Now let's do multiplication
# This one is trickier so here is the solution step by step

banner("Multiplication", char="*")
MUL = lambda a: lambda b: ... # it takes two numbers a and b
MUL = lambda a: lambda b: (lambda f: ... ) # it will return a number with its function bound to f
# MUL = lambda a: lambda b: (lambda f: ...(a(f))) # it returns a number that applies f a times
MUL = lambda a: lambda b: (lambda f: b(a(f))) # it needs to apply a(f) b times

# Let's test MUL
NINE = MUL(THREE)(THREE)
TEN = MUL(FIVE)(TWO)
TWELVE = MUL(THREE)(FOUR)
SIXTEEN = MUL(FOUR)(FOUR)
print(f"{NINE(inc)(0) = }")    # 9
print(f"{TEN(inc)(0) = }")     # 10
print(f"{TWELVE(inc)(0) = }")  # 12
print(f"{SIXTEEN(inc)(0) = }") # 16
assert NINE(inc)(0) == 9
assert TEN(inc)(0) == 10
assert TWELVE(inc)(0) == 12
assert SIXTEEN(inc)(0) == 16

# Finally, let's do exponentiation
banner("Exponentiation", char="*")
EXP = lambda a: lambda b: ... # it takes two numbers a and b
EXP = lambda a: lambda b: b(...) # it needs to apply b times ...
EXP = lambda a: lambda b: b(a) # it needs to apply b times a (times f but thats implicit)

# Let's test EXP
SIXTEEN_v2 = EXP(TWO)(FOUR) # 2^4
EIGHTYONE = EXP(THREE)(FOUR) # 3^4
SIXTYFOUR = EXP(FOUR)(THREE) # 4^3
print(f"{SIXTEEN_v2(inc)(0) = }") # 16
print(f"{EIGHTYONE(inc)(0) = }")  # 81
print(f"{SIXTYFOUR(inc)(0) = }")  # 64
assert SIXTEEN_v2(inc)(0) == 16
assert EIGHTYONE(inc)(0) == 81
assert SIXTYFOUR(inc)(0) == 64
