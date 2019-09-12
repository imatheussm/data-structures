from btree.constants import *


def insert_crescent(element, array):
    """Inserts an element in a list maintaining the numbers in crescent order.
    
    Parameters
    ----------
    element: int, float
        The element to be inserted.
    array: list
        The list into which the element shall be inserted.
    """
    print("[helper.insert_crescent()] Element: {}. Array: {}".format(element, array))
    if len(array) == 0:
        array.append(element)
        return
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
        return (
            obj.__module__ == "btree." + class_name and type(obj).__name__ == class_name
        )
    except:
        return False


def merge_to_list(*args):
    final_list = []
    for element in args:
        if type(element) in SUPPORTED_LIST_TYPES:
            for item in element:
                final_list.extend(merge_to_list(item))
        elif type(element) in SUPPORTED_TYPES:
            final_list.append(element)
    return final_list