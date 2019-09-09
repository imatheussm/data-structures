class RootPage:
    """The B-Tree itself."""
    
    def __init__(self, min_keys, *args):
        self.min_keys, self.max_keys = min_keys, 2 * min_keys
        
        for arg in args:
            