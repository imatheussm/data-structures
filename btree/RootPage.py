from btree.constants import *


class RootPage:
    """The root of the B-Tree."""

    def __init__(self, min_num_keys, *args):
        #self.depth = 0
        #self.height = 1
        self.keys = []
        self.level = self.depth + 1
        self.max_num_keys = 2 * min_num_keys
        self.min_num_keys = min_num_keys
        self.num_keys = 0

        for arg in args:
            self.insert(arg)

    def insert(self, element):
        """Inserts a number in the B-Tree."""

        if type(element) in SUPPORTED_LIST_TYPES:
            for item in element:
                self.insert(item)
        elif type(element) in SUPPORTED_TYPES:
            self.keys.append(element)
        else:
            raise TypeError(
                "This type is not supported. Type of the element: {}".format(
                    type(element)
                )
            )