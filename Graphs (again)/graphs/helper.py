def flatten(array):
    new_array = []

    for element in array:
        new_array.extend(element)

    return new_array