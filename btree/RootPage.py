from btree.constants import *
from btree.Page import *
from time import sleep


class RootPage(Page):
    """The root of the B-Tree."""

    def __init__(self, min_num_keys, parent_tree=None):
        super().__init__(min_num_keys, parent_tree, None)

    def get_left_page(self):
        return None
    
    def get_right_page(self):
        return None