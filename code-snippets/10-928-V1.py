# https://raw.githubusercontent.com/TheAlgorithms/Python/master/sorts/pigeon_sort.py
def pigeon_sort(array: list[int]) -> list[int]:
    """
    Implementation of pigeon hole sort algorithm
    :param array: Collection of comparable items
    :return: Collection sorted in ascending order
    >>> pigeon_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort([])
    []
    >>> pigeon_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    if len(array) == 0:
        return array

    _min, _max = min(array), max(array)

    # Compute the variables
    holes_range = _max - _min + 1
    holes, holes_repeat = [0] * holes_range, [0] * holes_range

    # Make the sorting.
    for i in array:
        index = i - _min
        holes[index] = i
        holes_repeat[index] += 1

    # Makes the array back by replacing the numbers.
    index = 0
    for i in range(holes_range):
        while holes_repeat[i] > 0:
            array[index] = holes[i]
            index += 1
            holes_repeat[i] -= 1

    # Returns the sorted array.
    return array
# # # # # delimiter # # # # # # #
print(pigeon_sort([0, 7, 4, 1, 1]))
