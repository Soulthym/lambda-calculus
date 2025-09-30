from slide_01_boolean import *
from slide_02_numbers import *
# This formalism lacks one important operation: predecessor
# We can apply one more time, but not one less time
# This is a problem for functions like factorial that need to go down to zero
# How can we implement PRED?
# We can use pairs to keep track of two numbers at once:
# - the first is the current number
# - the second is the predecessor (with pred(0) = 0)
# We will use need a trick to implement pairs
# Remember how we implemented booleans?
# They select between two alternatives
# We can use the same trick to implement pairs

# A pair is a function that takes a selector function f
# and applies it to the two elements of the pair
PAIR = lambda a: lambda b: lambda f: f(a)(b)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)
# Let's test our pairs
p = PAIR(3)(4)
print(f"{FIRST(p) = }")  # 3
print(f"{SECOND(p) = }") # 4
assert FIRST(p) == 3
assert SECOND(p) == 4

# Now we can implement PREV, which takes a pair (n, _) and returns (n+1, n)
PREV = lambda p: PAIR(SUCC(FIRST(p)))(FIRST(p))
START = PAIR(ZERO)(ZERO)
THREE_PAIR = FOUR(PREV)(START)
print(f"{FIRST(THREE_PAIR)(inc)(0) = }")  # 3
print(f"{SECOND(THREE_PAIR)(inc)(0) = }") # 2
assert FIRST(THREE_PAIR)(inc)(0) == 4
assert SECOND(THREE_PAIR)(inc)(0) == 3

# Finally, we can implement PRED using PREV
PRED = lambda n: SECOND(n(PREV)(START))
# Let's test PRED
THREE_PRED = PRED(FOUR)
TWO_PRED = PRED(THREE)
ONE_PRED = PRED(TWO)
ZERO_PRED = PRED(ONE)
print(f"{THREE_PRED(inc)(0) = }")  # 3
print(f"{TWO_PRED(inc)(0) = }")    # 2
print(f"{ONE_PRED(inc)(0) = }")    # 1
print(f"{ZERO_PRED(inc)(0) = }")   # 0
assert THREE_PRED(inc)(0) == 3
assert TWO_PRED(inc)(0) == 2
assert ONE_PRED(inc)(0) == 1
assert ZERO_PRED(inc)(0) == 0
# Houray!

banner("Substraction", char="*")
# Now that we have PRED, we can implement substraction
SUB = lambda a: lambda b: b(PRED)(a)
# Let's test SUB

SIX = SUCC(FIVE)

TWO_SUB_ONE = SUB(TWO)(ONE)
FIVE_SUB_THREE = SUB(FIVE)(THREE)
SIX_SUB_THREE = SUB(SIX)(THREE)
print(f"{TWO_SUB_ONE(inc)(0) = }")      # 1
print(f"{FIVE_SUB_THREE(inc)(0) = }")   # 2
print(f"{SIX_SUB_THREE(inc)(0) = }")    # 3
assert TWO_SUB_ONE(inc)(0) == 1
assert FIVE_SUB_THREE(inc)(0) == 2
assert SIX_SUB_THREE(inc)(0) == 3

# Now that we have substraction, we can implement IS_ZERO
IS_ZERO = lambda n: n(...)(TRUE) # return True if n is FALSE (which is identical to ZERO)
IS_ZERO = lambda n: n(lambda x: FALSE)(TRUE) # numbers take a function to apply, that function will return FALSE if applied at least once, otherwise we return TRUE

# Let's test IS_ZERO
print(f"{IS_ZERO(ZERO) = }")  # TRUE
print(f"{IS_ZERO(ONE) = }")   # FALSE
print(f"{IS_ZERO(TWO) = }")   # FALSE
assert IS_ZERO(ZERO) == TRUE
assert IS_ZERO(ONE) == FALSE
assert IS_ZERO(TWO) == FALSE
