from btree.helper import *
from btree.Page import *

class DegreeOverflowError(Exception):
    """Error that happens when a B-Tree has too many keys."""

    default_message = "The number of elements has surpasses the maximum amount allowed. Deploying measures..."

    def __init__(self, page, tree=None, message=default_message):
        super().__init__(message)