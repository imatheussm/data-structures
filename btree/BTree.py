from btree.RootPage import *


class BTree:
    """The B-Tree object per se."""

    def __init__(self, min_num_keys, *args):
        self.root = RootPage(min_num_keys, self, None, *args)

    def promoteRoot(self, page):
        middle_index = int((len(page.keys) - 1) / 2)
        print("middle_index: {}".format(middle_index))
        left_child = page.keys[:middle_index]
        right_child = page.keys[middle_index + 1 :]
        page.keys = [middle_index]
        try:
            if page.descendent_pages and len(page.descendent_pages) != 0:
                print("CUIDADO COM OS PONTEIROS! TEM FILHO AQUI!")
        except AttributeError:
            page.descendent_pages = [
                Page(page.min_num_keys, page.parent_tree, page, None, left_child),
                Page(page.min_num_keys, page.parent_tree, page, None, right_child),
            ]