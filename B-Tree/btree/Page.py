from btree.helper import *
from btree.constants import *
from btree.DegreeOverflowError import *
from btree.DegreeUnderflowError import *


class Page:
    """A Page of the B-Tree."""

    def __init__(self, min_num_keys, parent_tree, parent_page):
        """The construtor of the Page class.

        Paramters
        ---------

        self : Page

            A Page object.

        min_num_keys : int

            The degree of the B-Tree. This number influences in how short or long the list of keys must be in order to raise DegreeOverflowError or DegreeUnderflowError exceptions.

        parent_tree : BTree

            The BTree object to which the Page object relates.

        parent_page : Page

            The Page object which relates with the Page object to be created.

        Returns
        -------

        Page

            The resulting Page object.

        Methodology
        -----------

        This constructor basically sets a bunch of attributes according to the provided parameters.

        """
        self.descendent_pages = []
        self.keys = []
        self.max_num_keys = 2 * min_num_keys
        self.min_num_keys = min_num_keys
        self.num_keys = 0
        self.parent_page = parent_page
        if parent_tree:
            self.parent_tree = parent_tree

    def __contains__(self, element):
        """Tells if a given element is in the Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be searched for.

        Returns
        -------

        bool

            Whether the given element is stored in the Page object or not.

        Methodology
        -----------

        This method basically uses list.__contains__() with the provided parameter and returns the result.
        """
        return element in self.keys

    def __repr__(self):
        """The graphical representation of the Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        str

            The string representation of the Page, which generally is printed out by the Python interpreter.

        Methodology
        -----------

        This method just concatenates the list items into a single string and returns it.
        """
        return "[ " + " | ".join([(str(key)) for key in self.keys]) + " ]"

    def __len__(self):
        """Allows the use of len() with Page objects.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        int

            The number of keys contained under self.keys.

        Methodology
        -----------

        This method just calls len() with self.keys as a parameter and returns the result.
        """
        return len(self.keys)

    def __iter__(self):
        """The iterator of Page objects. Makes Page objects iterable.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        iter

            An iterable for the Page object.

        Methodology
        -----------

        This method just returns the iterable made by self.keys.
        """
        return iter(self.keys)

    def __getitem__(self, *args, **kwargs):
        """Allows use of slicing with Page objects.

        Parameters
        ----------

        self : Page

            A Page object.

        *args : list

            The arguments provided.

        **kwargs : dict

            The keyworded arguments provided.

        Returns
        -------

        SUPPORTED_TYPES, list

            The element whose index has been provided or a list of elements matching the limits provided.

        Methodology
        -----------

        This method passes all arguments to self.keys.__get__item(), which allows Page objects to have the same behavior of list object with regards to this method.
        """
        return self.keys.__getitem__(*args, **kwargs)

    def insert(self, element, will_raise=True):
        """Inserts a number in the B-Tree.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be inserted in the Page.

        will_raise : bool (default = True)

            Whether to verify for violations of B-Tree rules.

        Methodology
        ----------

        This method just inserts the element into self.keys and, if will_raise == True, checks for rule violations, raising a DegreeOverflowError if that is the case. This exception is handled by the BTree class.
        """
        insert_crescent(element, self.keys)
        self.num_keys += 1
        if will_raise and len(self.keys) > self.max_num_keys:
            raise DegreeOverflowError(self)

    def get_probable_descendent(self, element):
        """Returns the descennt page where a given element is expected to be.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be searched for.

        Returns
        -------

        Page, None

            The Page object in which the given element is expected to be found, or None, in case the Page object is a leaf page.

        Methodology
        -----------

        This method basically compares the keys of the page with the given element, returning the proper item of self.descendent_pages.

        This method is used by BTree.find() when searching for a given element, as it helps abstract the decision behind which descendent page to search next.
        """
        for i in range(len(self)):
            if self[i] > element:
                try:
                    return self.descendent_pages[i]
                except:
                    return None
        try:
            return self.descendent_pages[len(self)]
        except:
            return None

    def remove(self, element, will_raise=True):
        """Removes an element of a Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be removed of the Page object.

        will_raise : bool (default = True)

            Whether to verify for violations of B-Tree rules.

        Methodology
        -----------

        This method just removes the element of self.keys and, if will_raise == True, checks for rule violations, raising a DegreeUnderflowError if that is the case. This exception is handled by the BTree class.
        """
        self.keys.remove(element)
        self.num_keys -= 1

        if will_raise and self.parent_page != None and len(self) < self.min_num_keys:
            raise DegreeUnderflowError(self)

    def index(self, *args, **kwargs):
        """Returns the index of a element in a Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        *args : list

            The arguments provided.

        **kwargs : dict

            The keyworded arguments provided.

        Returns
        -------

        int

            The index in which the given element is expected to be found in self.keys.

        Methodology
        -----------

        This method basically gives to Page objects the same behavior of list objects with regards to their .index() implementations.
        """
        return self.keys.index(*args, **kwargs)

    def get_adjacent_element(self, element, with_page=False):
        """Returns an adjacent element (predecessor or sucessor) of a given number.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be taken as reference for the search.

        with_page : bool (default = False)

            Whether to include, in the returned results, the Page along with the element.

        Returns
        -------

        SUPPORTED_TYPES

            The element found in the search.

        tuple : (element, page)

            element : SUPPORTED_TYPES

                The element found in the search.

            page : Page

                The Page object in which the element is stored.

            The results of the search.

        Methodology
        -----------

        This method basically calls Page.get_previous_element() and Page.get_next_element() and compares the results to decide on which element shall be returned.

        """
        previous_element, previous_page = self.get_previous_element(element, True)
        next_element, next_page = self.get_next_element(element, True)

        if len(next_page) > len(previous_page):
            if with_page:
                return (next_element, next_page)
            else:
                return next_element
        else:
            if with_page:
                return (previous_element, previous_page)
            else:
                return previous_element

    def get_previous_element(self, element, with_page=False):
        """Returns the predecessor of a given element.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be taken as reference for the search.

        with_page : bool (default = False)

            Whether to include, in the returned results, the Page along with the element.

        Returns
        -------

        SUPPORTED_TYPES

            The predecessor element found.

        tuple : (element, page)

            element : SUPPORTED_TYPES

                The predecessor element found.

            page : Page

                The Page object in which the predecessor element is stored.

        Methodology
        -----------

        This method basically follows the rule and gets the rightmost element of the left descendent page of the Page object.
        """
        index = self.index(element)
        new_pointer = self.descendent_pages[index]

        while new_pointer:
            pointer = new_pointer
            try:
                new_pointer = pointer.descendent_pages[-1]
            except IndexError:
                if with_page:
                    return (pointer[-1], pointer)
                else:
                    return pointer[-1]

    def get_next_element(self, element, with_page=False):
        """Returns the sucessor of a given element.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be taken as reference for the search.

        with_page : bool (default = False)

            Whether to include, in the returned results, the Page along with the element.

        Returns
        -------

        SUPPORTED_TYPES

            The sucessor element found.

        tuple : (element, page)

            element : SUPPORTED_TYPES

                The sucessor element found.

            page : Page

                The Page object in which the sucessor element is stored.

            The results of the search.

        Methodology
        -----------

        This method basically follows the rule and gets the leftmost element of the right descendent page of the Page object.
        """
        index = self.index(element)
        new_pointer = self.descendent_pages[index + 1]

        while new_pointer:
            pointer = new_pointer
            try:
                new_pointer = pointer.descendent_pages[0]
            except IndexError:
                if with_page:
                    return (pointer[0], pointer)
                else:
                    return pointer[0]

    def get_adjacent_pages(self):
        """Returns the adjacent pages of a Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        tuple : (left_page, right_page)

            left_page : Page, None

                The left page of the Page object, or None if there is not any.

            right_page : Page, None

                The right page of the Page object, or None if there is not any.

            The results of the search.

        Methodology
        -----------

        This method basically calls Page.get_left_page() and Page.get_right_page() and returns both results under a tuple object.
        """
        try:
            left_page = self.get_left_page()
        except:
            left_page = None

        try:
            right_page = self.get_right_page()
        except:
            right_page = None

        return (left_page, right_page)

    def get_left_page(self):
        """Returns the page at the left of a Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        Page, None

            The page at the left of the Page object, or None if there is not any.

        Methodology
        -----------

        This method basically finds the Page index under page.parent_page.descendent_pages and gets the element in the same list that is immediately before the Page object. If that is not possible, None is returned.
        """
        if self.parent_page == None:
            return None
        else:
            page_pointer_index = self.parent_page.descendent_pages.index(self)
            if page_pointer_index == 0:
                return None
            else:
                return self.parent_page.descendent_pages[page_pointer_index - 1]

    def get_right_page(self):
        """Returns the page at the right of a Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        Page, None

            The Page at the right of the Page object, or None if there is not any.

        Methodology
        -----------

        This method basically finds the Page index under page.parent_page.descendent_pages and gets the element in the same list that is immediately after the Page object. If that is not possible, None is returned.
        """
        if self.parent_page == None:
            return None
        else:
            page_pointer_index = self.parent_page.descendent_pages.index(self)
            if page_pointer_index == len(self.parent_page):
                return None
            else:
                return self.parent_page.descendent_pages[page_pointer_index + 1]

    def can_get_borrowed(self):
        """Returns how many elements can be borrowed from a Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        int

            The number of elements that can be borrowed from the Page object by adjacent Page objects.

        Methodology
        -----------

        If the Page object in question does not have any descendents, the result returned is the difference between len(self.keys) (or just len(self)) and self.min_num_keys. Otherwise, 0 is returned.
        """
        if self.is_leaf():
            return len(self) - self.min_num_keys
        else:
            return 0

    def can_borrow(self, with_excedent_number=False):
        """Tells whether a Page object can borrow elements from adjacent Page objects.

        Parameters
        ----------

        self : Page

            A Page object.

        with_excedent_number : bool (default = False)

            Whether to return the number of elements that can be borrowed instead of a boolean result.

        Returns
        -------

        bool

            Whether the Page object can borrow elements from adjacent Page objects or not.

        tuple : (can_borrow_left, can_borrow_right)

            can_borrow_left : int

                How many elements can be borrowed from the left page.

            can_borrow_right : int

                How many elements can be borrowed from the right page.
        """
        if with_excedent_number == True:
            return (self.can_borrow_left(), self.can_borrow_right())
        else:
            return bool(self.can_borrow_left() or self.can_borrow_right())

    def can_borrow_left(self):
        """Tells whether a Page object can borrow elements from the left Page object (if there is any).

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        int

            How many elements can be borrowed from the left Page object by the Page object.

        Methodology
        -----------

        This method basically calls the Page.can_get_borrowed() method of the left Page object (obtained through Page.get_left_page()).
        """
        try:
            return self.get_left_page().can_get_borrowed()
        except:
            return 0

    def can_borrow_right(self):
        """Tells whether a Page object can borrow elements from the right Page object (if there is any).

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        int

            How many elements can be borrowed from the right Page object by the Page object.

        Methodology
        -----------

        This method basically calls the Page.can_get_borrowed() method of the right Page object (obtained through Page.get_right_page()).
        """
        try:
            return self.get_right_page().can_get_borrowed()
        except:
            return 0

    def borrow(self):
        """Borrows an element from an adjacent Page object, if possible.

        Parameters
        ----------

        self : Page

            A Page object.

        Methodology
        -----------

        This method calls Page.can_borrow() and compares the results to decide on which adjacent Page object to borrow from, calling either Page.borrow_left() or Page.borrow_right().
        """
        borrow_possibilities = self.can_borrow(True)

        if borrow_possibilities[0] > borrow_possibilities[1]:
            self.borrow_left()
        elif borrow_possibilities[1] > borrow_possibilities[0]:
            self.borrow_right()
        elif borrow_possibilities[0] > 0:
            self.borrow_left()
        else:
            raise Exception("Cannot borrow!")

    def borrow_left(self):
        """Borrows an element from the left Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Methodology
        -----------

        This method gets an element of the left Page object and moves it to page.parent_page, so that the element in its place can be brought down to the Page object.
        """
        page_index = self.parent_page.descendent_pages.index(self)
        left_page = self.get_left_page()
        element_to_borrow = left_page[-1]
        middle_element = self.parent_page[page_index - 1]
        left_page.remove(element_to_borrow)
        self.parent_page.keys[page_index - 1] = element_to_borrow
        self.insert(middle_element)

    def borrow_right(self):
        """Borrows an element from the right Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        Methodology
        -----------

        This method gets an element of the right Page object and moves it to page.parent_page, so that the element in its place can be brought down to the Page object.
        """
        page_index = self.parent_page.descendent_pages.index(self)
        right_page = self.get_right_page()
        element_to_borrow = right_page[0]
        middle_element = self.parent_page[page_index]
        right_page.remove(element_to_borrow)
        self.parent_page.keys[page_index] = element_to_borrow
        self.insert(middle_element)

    def get_pages_of_depth(self, depth, current_pointer=None, current_depth=0):
        """Returns all keys of Pages in the same depth.

        Parameters
        ----------

        self : Page

            A Page object.

        depth : int

            The depth in which the desired Page objects are located.

        current_pointer : Page, None (default = None)

            The pointer to the current Page object. If set to None, the Page object will be set as current_pointer.

        current_depth : int (default = 1)

            The current depth under analysis. If set to None, 1 will be set as the current_depth.

        Returns
        -------

        list

            The list of elements of the Page objects located in the desired depth.

        Methodology
        -----------

        This method basically goes down recursively through the descendent Page objects until it reaches the desired depth. These results are recursively appended into a list, which is returned at the end of the execution.
        """
        pages = []

        if not current_pointer:
            current_pointer = self

        if current_depth < depth:
            if len(current_pointer.descendent_pages) > 0:
                for descendent in current_pointer.descendent_pages:
                    pages.append(
                        self.get_pages_of_depth(depth, descendent, current_depth + 1)
                    )
                return pages
            else:
                raise ValueError("The tree is not that tall!")
        else:
            return current_pointer.keys

    def is_leaf(self):
        """Tells if a Page object is a leaf page.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        bool:

            Whether the Page object is a leaf page or not.

        Methodology
        -----------

        This method actually tells whether the self.descendent_pages attribute is an empty list or not.
        """
        return self.descendent_pages == []

    def is_root(self):
        """Tells if a Page object is a root page.

        Parameters
        ----------

        self : Page

            A Page object.

        Returns
        -------

        bool:

            Whether the Page object is a root page or not.

        Methodology
        -----------

        This method actually tells whether the self.parent_page attribute is None or not.
        """
        return self.parent_page == None

    def replace_with_leaf_element(self, element):
        """Replace an element of the Page object with a element in a leaf Page object.

        Parameters
        ----------

        self : Page

            A Page object.

        element : SUPPORTED_TYPES

            The element to be replaced with an element from a leaf Page object.

        Methodology
        -----------

        This method calls Page.get_adjacent_element() to get the best element to replace the one in the Page object, and proceeds with the replacement process. Then, it updates the references of the descendent Page objects, and raises a DegreeUnderflowError if the leaf Page from which an element has been taken now violates the B-Tree rules.

        """
        number, number_page = self.get_adjacent_element(element, with_page=True)
        number_page.remove(number, will_raise=False)
        self.keys[self.index(element)] = number

        self.update_descendents_parent_references()

        if len(number_page) < number_page.min_num_keys:
            raise DegreeUnderflowError(number_page)

    def update_descendents_parent_references(self):
        """Updates the Page.parent_page attribute of Page objects in Page.descendent_pages.

        Parameters
        ----------

        self : Page

            A Page object.

        Methodology
        -----------

        This method iterates through all elements of self.descendent_pages, setting their parent_page attribute to the Page object.
        """
        for descendent in self.descendent_pages:
            descendent.parent_page = self
