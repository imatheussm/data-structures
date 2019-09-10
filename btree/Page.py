import btree.helper as helper
from btree.RootPage import *
from btree.DegreeOverflow import *

class Page:
    """A Page of the B-Tree.
    
    This page is inherited by RootPage and LeafPage classes.
    """
    
    def __init__(self, min_num_keys, parent_tree=None, *args):
        # self.depth = 0
        # self.height = 1
        # self.level = self.depth + 1
        self.keys = []
        self.max_num_keys = 2 * min_num_keys
        self.min_num_keys = min_num_keys
        self.num_keys = 0
        self.parent_tree = parent_tree
        
        for arg in args:
            self.insert(arg)
            
    def insert(self, element):
        """Inserts a number in the B-Tree."""

        if type(element) in SUPPORTED_LIST_TYPES:
            for item in element:
                self.insert(item)
            return
        elif type(element) in SUPPORTED_TYPES:
            if len(self.keys) == 0:
                self.keys.append(element)
            else:
                helper.insert_crescent(element, self.keys)
        else:
            raise TypeError(
                "This type is not supported. Type of the element: {}".format(
                    type(element)
                )
            )
        self.num_keys += 1
        
        if len(self.keys) > self.max_num_keys:
            raise DegreeOverflow(self)