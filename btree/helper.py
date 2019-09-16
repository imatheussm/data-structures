from btree.constants import *


def insert_crescent(element, array):
    """Inserts an element in a list maintaining the numbers in crescent order.
    
    Parameters
    ----------
    
    element: int, float
    
        The element to be inserted.
        
    array: list
    
        The list into which the element shall be inserted.
        
    Methodology
    -----------
    
    This function compares the given element against the elements of the given array, searching for the appropriate spot to insert it.
    """
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
    """Tells if an object is of a given class (given as a string).
    
    Parameters
    ----------
    
    obj : object
    
        The object to be analysed.
        
    class_name : str
    
        The string name of the class to be checked against.
        
    Returns
    -------
    
    bool
    
        Whether the object is of the given class or not.
        
    Methodology
    -----------
    
    This function has been taken from a StackOverflow answer and modified accordingly. It basically compares aspects of the object in question under the Python namespace. 
    """
    try:
        return (
            obj.__module__ == "btree." + class_name and type(obj).__name__ == class_name
        )
    except:
        return False


def merge_to_list(*args):
    """Merges elements of various list types and types into an one-dimensional list.
    
    Parameters
    ----------
    
    *args : list
    
        The elements to be merged.
        
    Returns
    -------
    
    list
    
        An one-dimensional list with all the elements provided.
        
    Methodology
    -----------
    
    This function basically calls itself recursively to get deeper and deeper into the provided list structures and obtain only the elements contained in them. They are returned to extend the final_list list, which is returned at the end of execution.
    """
    final_list = []
    for element in args:
        if type(element) in SUPPORTED_LIST_TYPES:
            for item in element:
                final_list.extend(merge_to_list(item))
        else:
            final_list.append(element)
    return final_list


def merge_to_list_of_lists(*args):
    """Merges elements of various list types and types into a two-dimensional list.
    
    Parameters
    ----------
    
    *args : list
    
        The elements to be merged.
        
    Returns
    -------
    
    list
    
        The list of lists with all the elements provided.
        
    Methodology
    -----------
    
    This function does pretty much the same thing as merge_to_list(), with the difference that this function stops just before entering the last list, appending it instead to final_list, which is returned at the end of execution. This function calls itself recursively as well.
    """
    final_list = []
    for element in args:
        if type(element) in SUPPORTED_LIST_TYPES:
            try:
                if type(element[0]) in SUPPORTED_LIST_TYPES:
                    for item in element:
                        final_list.extend(merge_to_list_of_lists(item))
                else:
                    final_list.append(element)
            except IndexError:
                final_list.append([])
    return final_list
