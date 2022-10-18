# https://raw.githubusercontent.com/TheAlgorithms/Python/master/maths/power_using_recursion.py
def foo(a: int, b: int) -> float:
    return a * foo(a, (b - 1)) if b else 1

# # # # # delimiter # # # # # # #
print(foo(2, 3))
