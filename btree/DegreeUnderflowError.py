from btree.helper import *
from btree.Page import *


class DegreeUnderflowError(Exception):
    """Error that happens when a B-Tree has too few keys."""

    default_message = (
        "The number of elements is below the minimum allowed. Deploying measures..."
    )

    def __init__(self, page, message=default_message):
        """The constructor of the DegreeUnderflowError exception class.
        
        Parameters
        ----------
        
        self : DegreeUnderflowError
        
            A DegreeUnderflowError object.
            
        page : Page
        
            A Page object which has caused the DegreeUnderflowError.
            
        message : str (default = default_message)
        
            The message to be displayed when raising the DegreeUnderflowError (considering it is not treated by another class or something).
            
        Returns
        -------
        
        DegreeUnderflowError
        
            A DegreeUnderflowError object containing the Page that caused this exception.
        """
        super().__init__(message)
        self.page = page
        self.tree = page.parent_tree
