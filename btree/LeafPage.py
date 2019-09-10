from btree.Page import *


class LeafPage(Page):
    """The root of the B-Tree."""

    def __init__(
        self,
        min_num_keys,
        parent_tree=None,
        parent_page=None,
        descendent_pages=None,
        *args,
    ):
        super().__init__(
            min_num_keys, parent_tree, parent_page, descendent_pages, *args
        )
        del self.descendent_pages

