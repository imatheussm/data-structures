class DegreeOverflow(OverflowError):
    """Error that happens when a B-Tree has too many keys."""

    def __init__(self, page, message):
        super().__init__(message)

        # CREATE HANDLING OF OVERFLOW (MANY ITEMS IN LIST)