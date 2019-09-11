def insert_crescent(element, array):
    """Inserts an element in a list maintaining the numbers in crescent order.
    
    Parameters
    ----------
    element: int, float
        The element to be inserted.
    array: list
        The list into which the element shall be inserted.
    """
    if len(array) == 0:
        array.append(element)
    for (index, key) in enumerate(array):
        if element > key:
            continue
        else:
            array.insert(index, element)
            return
    array.append(element)
    return


def is_class(obj, class_name):
    try:
        return obj.__module__ == "btree." + class_name and type(obj).__name__ == class_name
    except:
        return False
