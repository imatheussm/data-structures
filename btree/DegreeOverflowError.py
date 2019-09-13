from btree.helper import *
from btree.Page import *


class DegreeOverflowError(Exception):
    """Error that happens when a B-Tree has too many keys."""

    default_message = (
        "The number of elements surpasses the maximum allowed. Deploying measures..."
    )

    def __init__(self, page, message=default_message):
        super().__init__(message)
        self.page = page
        self.tree = page.parent_tree
        
        # print("[DegreeOverflowError.__init__()] Degree overflow!")
        # print("[DegreeOverflowError.__init__()] page: {}".format(page))
        # try: print("[DegreeOverflowError.__init__()] page.parent_page: {}".format(page.parent_page))
        # except: pass