# https://raw.githubusercontent.com/python/cpython/main/Tools/c-analyzer/c_common/iterutil.py
def foo(quux):
    if not quux:
        return None, None
    quux = iter(quux)
    try:
        garply = next(quux)
    except StopIteration:
        return None, None
    def bar():
        yield garply
        yield from quux
    return bar(), garply
# # # # # delimiter # # # # # # #
quux = ["item1", "item2", "item3"]
grault, garply = foo(quux)

for waldo in grault:
    print(waldo)