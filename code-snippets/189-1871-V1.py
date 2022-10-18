# https://raw.githubusercontent.com/python/cpython/main/Tools/c-analyzer/c_common/iterutil.py
def peek_and_iter(items):
    if not items:
        return None, None
    items = iter(items)
    try:
        peeked = next(items)
    except StopIteration:
        return None, None
    def chain():
        yield peeked
        yield from items
    return chain(), peeked
# # # # # delimiter # # # # # # #
items = ["item1", "item2", "item3"]
chain, peeked = peek_and_iter(items)

for element in chain:
    print(element)