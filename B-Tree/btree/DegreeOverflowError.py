from btree.helper import *
from btree.Page import *


class DegreeOverflowError(Exception):
    """Error that happens when a B-Tree has too many keys."""

    default_message = (
        "The number of elements surpasses the maximum allowed. Deploying measures..."
    )

    def __init__(self, page, message=default_message):
        """The constructor of the DegreeOverflowError exception class.
        
        Parameters
        ----------
        
        self : DegreeOverflowError
        
            A DegreeOverflowError object.
            
        page : Page
        
            A Page object which has caused the DegreeOverflowError.
            
        message : str (default = default_message)
        
            The message to be displayed when raising the DegreeOverflowError (considering it is not treated by another class or something).
            
        Returns
        -------
        
        DegreeOverflowError
        
            A DegreeOverflowError object containing the Page that caused this exception.
        """
        super().__init__(message)
        self.page = page
        self.tree = page.parent_tree
