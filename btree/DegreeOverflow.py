from btree.RootPage import *


class DegreeOverflow(OverflowError):
    """Error that happens when a B-Tree has too many keys."""

    default_message = "The number of elements has surpasses the maximum amount allowed. Deploying measures..."

    def __init__(self, page, message=default_message):
        super().__init__(message)

        if type(page) == RootPage:
            self.promoteRoot(page)

    def promoteRoot(self, page):
        middle_index = (len(page.keys) - 1) / 2
        left_child = page.keys[:middle_index]
        right_child = page.keys[middle_index + 1 :]
        page.keys = [middle_index]
        try:
            if page.descendent_pages:
                print("CUIDADO COM OS PONTEIROS! TEM FILHO AQUI!")
                raise NameError
        except NameError:
            page.descendent_pages = [
                Page(page.min_num_keys, page.parent_tree, page, None, left_child),
                Page(page.min_num_keys, page.parent_tree, page, None, right_child),
            ]

