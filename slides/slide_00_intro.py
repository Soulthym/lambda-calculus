from lc.lc import *

# First a bit of history:
# Alonzo Church (1903-1995) was a computer scientist, mathematician and logician
# He invented lambda calculus in the 1930s as part of his research into the foundations of mathematics
# He notably showed that the lambda calculus is Turing complete
# (and that turing machines are 'lambda complete' too),
# and that the halting problem is undecidable
# He also invented Church encoding, a means of representing data and operators in the lambda calculus
# This presentation is an exploration of his work

# Let's take a simple Python function, a factorial
# fact(0) = 1
# fact(n) = n * fact(n-1)
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)

print(f"{fact(5) = }")

# How far can we abstract this function?
# Let's start with the if statement
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

# Let's test our code
# print(f"{fact(5) = }") # Uncomment this

# Oh no, we blew up the stack!
# Why did that happen?
# Because pyhon is an eager language, it evaluates function arguments before calling the function
# This means that even if we hit the base case of fact,
# we still need to evaluate n * fact(n - 1) before we can return the result,
# which means we need to evaluate fact(n - 1), and so on... forever
# We will address this point at the end of this presentation
# for now, we will not run the fact function and only
# focus on the rest of the code

