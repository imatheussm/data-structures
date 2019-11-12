def flatten(array):
    """Turns a two-dimensional array into a one-dimensional one.

    Parameters
    ----------

    array : list

        The array to be flattened.

    Returns
    -------

    list

        The flattened array.
    """
    new_array = []

    for element in array:
        new_array.extend(element)

    return new_array
