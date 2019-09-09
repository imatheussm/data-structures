from btree.RootPage import *

class BTree:
    """The B-Tree object per se."""
    
    def __init__(self, min_num_keys, *args):
        self.root = RootPage(min_num_keys, *args)
        self.height = 0