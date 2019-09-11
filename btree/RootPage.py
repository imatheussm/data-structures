from btree.constants import *
from btree.Page import *
from time import sleep


class RootPage(Page):
    """The root of the B-Tree."""

    def __init__(
        self,
        min_num_keys,
        parent_tree=None,
        descendent_pages=None,
        *args
    ):
        super().__init__(
            min_num_keys, parent_tree, None, descendent_pages, *args
        )
        del self.parent_page

