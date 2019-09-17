# from btree.RootPage import *
from btree.helper import *
from btree.Page import *


class BTree:
    """The B-Tree object per se."""

    def __init__(self, min_num_keys, *args):
        """The BTree class constructor.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        min_num_keys : int
        
            The degree of the tree. This value will be applied to all Page objects and objects of Page subclasses as well.
            
        *args : list
        
            The elements to be inserted. Any further treatment and measures shall be taken by BTree.insert().
        
        Returns
        -------
        
        BTree
        
            A BTree object containing the values from *args and the degree stated in min_num_keys.
            
        Methodology
        -----------
        
        This constructor initializes the BTree object, which in turn initializes a Page object to be its root attribute.
        
        If there are any additional arguments under *args, they will be inserted sequentially in the BTree object through Btree.insert().
        """
        self.root = Page(min_num_keys, self, None)
        self.num_keys = 0

        self.insert(*args)

    def insert(self, *args):
        """Inserts any amount of items into the BTree.

        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        *args : list
        
            The elements to be inserted. If there are lists with lists or similar cases, they will be merged into an one-dimensional list, and each element of this list will be inserted subsequently.
            
        Methodology
        -----------
        
        After merging *args into an one-dimensional list through merge_to_list(), the method will verify if each item is a supported type: if not, a TypeError will be raised.
        
        Then, BTree.find() will be called to see if the element is already in the BTree object. If it is, a message will be printed and the loop will move to the next item. Otherwise, Page.insert() will be called to insert the element into the closest page BTree.find() returned.
        
        If a DegreeOverflowError is raised by Page.insert(), BTree.promote() will be called with the page that needed measures to be taken as a parameter.
        """
        arguments = merge_to_list(args)
        for arg in arguments:
            if type(arg) in SUPPORTED_TYPES:
                in_tree, page_pointer, _ = self.find(arg)
                if in_tree:
                    raise ValueError(
                        "The value {} is already in the B-Tree.".format(arg)
                    )
                    continue
                try:
                    page_pointer.insert(arg)
                except DegreeOverflowError as e:
                    self.promote(e.page)
            else:
                raise TypeError(
                    "This type is not supported. Type of the argumenet: {}".format(
                        str(type(arg))
                    )
                )

            self.num_keys += 1

    def find(self, element):
        """Finds an element in the BTree object.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        element : Object
        
            An object to be found in the BTree.
        
        Returns
        -------
        
        tuple : (in_tree, page_pointer)
        
            in_tree : bool
            
                Tells if the item is in the BTree object.
                
            page_pointer : Page
            
                If in_tree == True, tells the page in which the element to be found is. Otherwise, tells the page in which the element was expected to be found.
                
            page_index : int
            
                The index in which the given element is stored in the page returned under page_pointer. If the element is not found, then the returned value will be -1.
                
        Methodology
        -----------
        
        This method will begin its search at self.root, which will be the initial value of the page_pointer variable. Then, it will ask the page if the given element is in the page_pointer Page object. If it is, it will return a tuple telling in the first element that it has been found (True), which is the page in which the element is stored in the second element (Page) and which is the index in which the element is stored (int). If it is not, the first element will be False, the Page returned will be the leaf page in which the method expected to find the element and the index returned will be -1.
        """
        page_pointer = self.root

        while True:
            if element in page_pointer:
                return (True, page_pointer, page_pointer.index(element))
            else:
                new_page_pointer = page_pointer.get_probable_descendent(element)
                if new_page_pointer:
                    page_pointer = new_page_pointer
                else:
                    return (False, page_pointer, -1)

    def promote(self, page):
        """Promotes an element one level above.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        page : Page
        
            A Page object containing the elements to be treated.

        Methodology
        -----------
        
        The method will begin by separating the keys and descendents that will go to each descendent page, as well as the middle key which will remain in the original page.
        
        It is with these values that the method creates two new pages, setting the parent_page attributes and inserting the respective descendents where they are supposed to be.
        
        Finally, it gives the two newly-created Page objects, the middle key of the current Page object and the Page object itself to self.promote_root_page() or self.promote_page(), depending on whether the Page object to be promoted is a root page or not.
        """
        middle_index = page.min_num_keys

        left_keys = page[:middle_index].copy()
        middle_key = page[middle_index]
        right_keys = page[middle_index + 1 :].copy()
        left_descendents = page.descendent_pages[: middle_index + 1]
        right_descendents = page.descendent_pages[middle_index + 1 :]

        left_child = left_child = Page(page.min_num_keys, self, None)
        right_child = Page(page.min_num_keys, self, None)
        left_child.descendent_pages = left_descendents
        right_child.descendent_pages = right_descendents

        for descendent in left_child.descendent_pages:
            descendent.parent_page = left_child
        for descendent in right_child.descendent_pages:
            descendent.parent_page = right_child

        for item in left_keys:
            left_child.insert(item)
        for item in right_keys:
            right_child.insert(item)

        if page.is_root():
            self.promote_root_page(page, left_child, middle_key, right_child)
        else:
            self.promote_page(page, left_child, middle_key, right_child)

    def promote_root_page(self, page, left_child, middle_key, right_child):
        """Promotes a root page.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        page : Page
            
            The Page object to be promoted.
            
        left_child : Page

            A Page object created by BTree.promote(), which will be set under the descendent_pages list to be the left pointer relative to the middle key element.
        
        middle_key : SUPPORTED_TYPES
            
            The middle element. It will be used as reference during the insertion of the left_child and right_child under the proper descendent_pages list attribute.
        
        right_child : Page
        
            A Page object created by BTree.promote(), which will be set under the descendent_pages list to be the right pointer relative to the middle key element.
            
        Methodology
        -----------
        
        Since it is the root page we are talking about, the process is relatively straightforward: it is just a matter of setting page.keys to be just the middle key element and the page.descendent_pages list to be just the two newly-created Page objects. The method finishes its job by telling the children who their parent is.
        """
        page.keys = [middle_key]
        page.descendent_pages = [left_child, right_child]
        left_child.parent_page = page
        right_child.parent_page = page

    def promote_page(self, page, left_child, middle_key, right_child):
        """Promotes a root page.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        page : Page
            
            The Page object to be promoted.
            
        left_child : Page

            A Page object created by BTree.promote(), which will be set under the descendent_pages list to be the left pointer relative to the middle key element.
        
        middle_key : SUPPORTED_TYPES
            
            The middle element. It will be used as reference during the insertion of the left_child and right_child under the proper descendent_pages list attribute.
        
        right_child : Page
        
            A Page object created by BTree.promote(), which will be set under the descendent_pages list to be the right pointer relative to the middle key element.
        
        Methodology
        -----------
        
        Although the goal of this method is virtually the same as BTree.promote_root_page(), its executions are quite different. The pages that fall under this method can be leaf pages or pages in intermediate levels. This is the most difficult case, since just a wrong pointer is enough to generate unexpected behavior during the use of this BTree object.
        
        First, the method saves the parent_page and eliminates the page object completely. The necessary information is already stored under the remaining parameters provided. Then, it inserts the middle_key in the parent_page, obtains the index in which the middle key element has been stored and uses it as reference to insert the left_child and right_child Page objects. It finishes its job by telling each descendent page who their parent is.
        
        Before wrapping it up, the method has to verify if there has been a violation of the B-Tree rules. It does so by verifying the proper methods and calling BTree.promote(), BTree.demote() or neither.
        """
        parent_page = page.parent_page
        parent_page.descendent_pages.remove(page)
        del page

        parent_page.insert(middle_key, will_raise=False)
        insertion_index = parent_page.index(middle_key)

        parent_page.descendent_pages.insert(insertion_index, right_child)
        parent_page.descendent_pages.insert(insertion_index, left_child)

        left_child.parent_page = parent_page
        right_child.parent_page = parent_page

        if len(parent_page) > parent_page.max_num_keys:
            self.promote(parent_page)
        elif not parent_page.is_root() and len(parent_page) < parent_page.min_num_keys:
            self.demote(parent_page)

    def demote(self, page):
        """Demotes a page of the BTree object.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        page : Page

            A Page object to be demoted.
            
        Methodology
        -----------
        
        At the beginning of the execution of this method, the parent_page and the index in which the page is stored under parent_page.descendent_pages are saved in parent_page and page_index, respectively. Then, it decides which sibling page will be part of the merge procedure, calling either BTree.demote_left() or BTree.demote_right(). 
        
        After these methods are done with their jobs, this method moves forward to a set of verifications: if, after this procedure, the parent_page violates the B-Tree minimum degree rule, then BTree.demote() is called with parent_page as a parameter. Otherwise, if parent_page actually is the root of the BTree object and its length is 0, it means that the height of the B-Tree has lowered, and the self.root attribute must be resetted. This is done by calling BTree.recreate_root().
        
        """
        parent_page = page.parent_page
        page_index = page.parent_page.descendent_pages.index(page)
        if page.get_left_page():
            self.demote_left(page, page_index)
        else:
            self.demote_right(page, page_index)

        if not parent_page.is_root() and len(parent_page) < parent_page.min_num_keys:
            self.demote(parent_page)

        elif parent_page.is_root() and len(parent_page) == 0:
            self.recreate_root()

    def demote_left(self, page, page_index):
        """Merges the page in question with the page at its left, taking an element from the parent page.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        page : Page
        
            The Page object which will undergo the merge procedure.
            
        page_index : int
        
            The index in which the page is stored in page.parent_page.descendent_pages.
            
        Methodology
        -----------
        
        After obtaining the parent page, the element to be taken from it and the left page, this method will move on to the proper page merge. Actually, what happens is that the left page receives the middle element taken from parent_page and the remaining elements from page, as well as the descendent pages of page. Then, page is removed and deleted.
        
        The method finishes by updating the descendents of the left page with regards to their parent and verifying whether the resulting left_page has surpassed the maximum number of keys it is allowed to store in the BTree object. If so, BTree.promote() is called with left_page as a parameter.
        """
        parent_page = page.parent_page
        left_page = page.get_left_page()
        middle_element = parent_page[page_index - 1]
        parent_page.remove(middle_element, will_raise=False)
        left_page.insert(middle_element, will_raise=False)
        for element in page:
            left_page.insert(element, will_raise=False)
        left_page.descendent_pages = left_page.descendent_pages + page.descendent_pages
        parent_page.descendent_pages.remove(page)
        del page

        left_page.update_descendents_parent_references()

        if len(left_page) > left_page.max_num_keys:
            self.promote(left_page)

    def demote_right(self, page, page_index):
        """Merges the page in question with the page at its right, taking an element from the parent page.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        page : Page
        
            The Page object which will undergo the merge procedure.
            
        page_index : int
        
            The index in which the page is stored in page.parent_page.descendent_pages.
            
        Methodology
        -----------
        
        After obtaining the parent page, the element to be taken from it and the right page, this method will move on to the proper page merge. Actually, what happens is that the right page receives the middle element taken from parent_page and the remaining elements from page, as well as the descendent pages of page. Then, page is removed and deleted.
        
        The method finishes by updating the descendents of the right page with regards to their parent and verifying whether the resulting right_page has surpassed the maximum number of keys it is allowed to store in the BTree object. If so, BTree.promote() is called with right_page as a parameter.
        """
        parent_page = page.parent_page
        right_page = page.get_right_page()
        middle_element = parent_page[page_index]
        parent_page.remove(middle_element, will_raise=False)
        right_page.insert(middle_element, will_raise=False)
        for element in page:
            right_page.insert(element, will_raise=False)
        right_page.descendent_pages = (
            page.descendent_pages + right_page.descendent_pages
        )
        parent_page.descendent_pages.remove(page)
        del page

        right_page.update_descendents_parent_references()

        if len(right_page) > right_page.max_num_keys:
            self.promote(right_page)

    def remove(self, *args):
        """Removes any amount of items of the BTree object.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        *args : list
        
            The elements to be removed. If there are lists with lists or similar cases, they will be merged into an one-dimensional list, and each element of this list will be inserted subsequently.
            
        Methodology
        -----------
            
        After merging *args into an one-dimensional list, BTree.find() will be called to see if the element is already in the BTree object. If it is not, an ValueError will be raised. Otherwise, the method will move forward to see if the Page is a leaf page or not by calling Page.is_leaf(). If it is, then it is just a matter of calling Page.remove() to remove the element of the page BTree.find() returned and deal with the possibility of a DegreeUnderflowError being raised. If it is not a leaf page, then the element stored in it has to be replaced with an adjacent element first. This is done by calling Page.replace_with_leaf_element(). The possibility of a DegreeUnderflowError exists here as well.
        
        If a DegreeUnderflowError is raised by Page.remove() or Page.replace_with_leaf_element(), BTree.demote() will be called with the page that needs measures to be taken as a parameter.
        """
        arguments = merge_to_list(args)
        for arg in arguments:
            in_tree, page_pointer, arg_index = self.find(arg)
            if in_tree == True:
                if page_pointer.is_leaf():
                    try:
                        page_pointer.remove(arg)
                    except DegreeUnderflowError as e:
                        if e.page.can_borrow():
                            e.page.borrow()
                        else:
                            self.demote(e.page)
                else:
                    try:
                        page_pointer.replace_with_leaf_element(arg)
                    except DegreeUnderflowError as e:
                        self.demote(e.page)
            else:
                raise ValueError("The value {} is not in this tree.".format(arg))

    def recreate_root(self):
        """Resets the self.root attribute of the BTree.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        Methodology
        -----------
        
        This method is executed when, during a BTree.demote() execution, the self.root Page has all of its keys removed. At this point, the root is actually its only descendent page. BTree.demote() verifies for this possibility, and if appropriate, it calls this method, which merely sets self.root to self.root.descendent_pages[0], sets self.root.parent_page to None and updates the descendent_pages accordingly.
        """
        if len(self.root.descendent_pages) > 1:
            raise ValueError("There's more than a root?")
        self.root = self.root.descendent_pages[0]
        self.root.parent_page = None
        self.root.update_descendents_parent_references()

    def __contains__(self, element):
        """Tells if the BTree object contains a given element.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        element : SUPPORTED_TYPES
        
            A supported element to be searched throughout the BTree object.
            
        Returns
        -------
        
        bool
            The result of the search, telling if the given element is in the BTree object or not.
            
        Methodology
        -----------
        
        This is just a wrapper to BTree.find(), but without the additional parameters returned by it.
        
        """
        return self.find(element)[0]

    def __repr__(self):
        """The visual representation of the BTree object.
        
        Parameters
        ----------
        
        self : BTree
            
            A BTree object.
            
        Returns
        -------
        
        str
            The visual representation of the BTree object, which normally is printed out to the console by the Python interpreter.
            
        Methodology
        -----------
        
        This method takes advantage of BTree.get_height() and BTree.get_pages_of_height(). It obtains all pages of each height and does some calculations to figure out how much space is to be added between the elements of each level. It stores the final result of each level as a string under representations, which at the end is merged (with each line separated by a line break) and returned.
        """
        height = self.get_height()
        representations = [
            " ".join([str(item) for item in self.get_pages_of_height(height)])
        ]
        max_length = len(representations[0])

        for h in range(height - 1, 0, -1):
            list_of_elements = self.get_pages_of_height(h)
            string_representation = " ".join(
                [str(item) for item in self.get_pages_of_height(h)]
            )
            list_length = len(list_of_elements)
            string_length = len(string_representation)
            number_of_spaces = int((max_length - string_length) / (list_length + 1))
            spaces = number_of_spaces * " "
            representation = (
                spaces
                + spaces.join([str(item) for item in self.get_pages_of_height(h)])
                + spaces
            )
            representations.insert(0, representation)

        representations.insert(0, object.__repr__(self))

        return "\n".join(representations)

    def get_height(self):
        """Returns the height of the BTree object.
        
        Parameters
        ----------
        
        self : BTree
        
            A BTree object.
            
        Returns
        -------
        
        int
            
            The height of the BTree object.
            
        Methodology
        -----------
        
        This method just calls BTree.get_pages_of_height() with 1 as a parameter, and increments the value by one unit until it returns None, taking note of the last number. At the end, it returns the height obtained.
        """
        height = 0
        while self.get_pages_of_height(height + 1):
            height += 1
        return height

    def get_pages_of_height(self, height, merge_lists=True):
        """Returns all pages in the same, given height.
        
        Parameters
        ----------
        
        self : BTree
            
            A BTree object.
            
        height : int
        
            The height to be consulted.
            
        merge_lists : bool (default = True)

            Whether to merge all lists in a list of lists through merge_to_list_of_lists().
            
        Returns
        -------
        
        list, None

            A list of lists containing the element (affected by the merge_lists parameter) or None, in case the height provided resulted in an empty list.
        """
        try:
            pages = self.root.get_pages_of_height(height)
            if merge_lists:
                return merge_to_list_of_lists(pages)
            else:
                return pages
        except:
            return None
