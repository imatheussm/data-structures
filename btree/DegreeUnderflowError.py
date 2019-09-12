from btree.helper import *
from btree.Page import *


class DegreeUnderflowError(Exception):
    """Error that happens when a B-Tree has too many keys."""

    default_message = "The number of elements is below the minimum allowed. Deploying measures..."

    def __init__(self, page, message=default_message):
        super().__init__(message)
        self.page = page
        self.tree = page.parent_tree
