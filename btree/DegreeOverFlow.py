class DegreeOverflow(OverflowError):
    """Error that happens when a B-Tree has too many keys."""

    default_message = "The number of elements has surpasses the maximum amount allowed. Deploying measures..."
    
    def __init__(self, page, message=default_message):
        super().__init__(message)

        # CREATE HANDLING OF OVERFLOW (MANY ITEMS IN LIST)