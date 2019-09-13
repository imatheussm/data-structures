from btree.RootPage import *
from btree.helper import *
from btree.DegreeOverflowError import *
from btree.LeafPage import *


class BTree:
    """The B-Tree object per se."""

    def __init__(self, min_num_keys, *args):
        """The BTree class constructor.
        
        Parameters
        ----------
        self: BTree
            A BTree object.
        min_num_keys: int
            The degree of the tree. This value will be applied to all Page objects and objects of Page subclasses as well.
        *args: list
            The elements to be inserted. Any further treatment and measures shall be taken by BTree.insert().
        
        Returns
        -------
        BTree
            A BTree object.
        """
        self.root = RootPage(min_num_keys, self)
        self.num_keys = 0

        self.insert(*args)

    def insert(self, *args):
        """Inserts any amount of items into the BTree.
        
        Parameters
        ----------
        self: BTree
            A BTree object.
        *args: list
            The elements to be inserted. If there are lists with lists or similar cases, they will be merged into an one-dimensional list, and each element of this list will be inserted subsequently.
            
        After merging *args into an one-dimensional list, the method will verify if each item is a supported type: if not, a TypeError will be raised.
        Then, BTree.find() will be called to see if the element is already in the BTree object. If it is, a message will be printed and the loop will move to the next item. Otherwise, Page.insert() will be called to insert the element into the closest page BTree.find() returned.
        If a DegreeOverflowError is raised by Page.insert(), BTree.promote() will be called with the page that needed measures to be taken as a parameter.
        """
        arguments = merge_to_list(args)
        for arg in arguments:
            if type(arg) in SUPPORTED_TYPES:
                in_tree, page_pointer = self.find(arg)
                if in_tree:
                    print("O valor {} já está na árvore.".format(arg))
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
        self: BTree
            A BTree object.
        element: Object
            An object to be found in the BTree.
        
        Returns
        -------
        tuple: (in_tree, page_pointer)
            in_tree: bool
                Tells if the item is in the BTree object.
            page_pointer: Page
                If in_tree == True, tells the page in which the element to be found is. Otherwise, tells the page in which the element was expected to be found.
        """
        page_pointer = self.root

        while True:
            if element in page_pointer:
                return (True, page_pointer)
            else:
                new_page_pointer = page_pointer.return_pointer(element)
                if new_page_pointer:
                    page_pointer = new_page_pointer
                else:
                    return (False, page_pointer)

    def promote(self, page):
        """Promotes a number one level above.
        
        Parameters
        ----------
        self: BTree
            A BTree object.
        page: Page
            A Page object containing the elements to be treated.
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

        for item in left_keys:
            left_child.insert(item)
        for item in right_keys:
            right_child.insert(item)

        if is_class(page, "RootPage"):
            self.promote_RootPage(page, left_child, middle_key, right_child)
        elif is_class(page, "Page"):
            self.promote_Page(page, left_child, middle_key, right_child)

    def promote_RootPage(self, page, left_child, middle_key, right_child):
        page.keys = [middle_key]
        page.descendent_pages = [left_child, right_child]

        self.update_parent_trees()

    def promote_Page(self, page, left_child, middle_key, right_child):
        parent_page = page.parent_page
        parent_page.descendent_pages.remove(page)
        del page

        parent_page.insert(middle_key, willRaise=False)
        insertion_index = parent_page.index(middle_key)

        parent_page.descendent_pages.insert(insertion_index, right_child)
        parent_page.descendent_pages.insert(insertion_index, left_child)

        self.update_parent_trees(parent_page)

        if len(parent_page) > parent_page.max_num_keys:
            self.promote(parent_page)

    def update_parent_trees(self, pointer=None):
        if not pointer:
            pointer = self.root

        if len(pointer.descendent_pages) > 0:
            for child in pointer.descendent_pages:
                try:
                    if child.parent_page != pointer:
                        child.parent_page = pointer
                except:
                    child.parent_page = pointer
                self.update_parent_trees(child)

    def remove(self, *args):
        """Removes any amount of items of the BTree object.
        
        Parameters
        ----------
        self: BTree
            A BTree object.
        *args: list
            The elements to be removed. If there are lists with lists or similar cases, they will be merged into an one-dimensional list, and each element of this list will be inserted subsequently.
            
        After merging *args into an one-dimensional list, BTree.find() will be called to see if the element is already in the BTree object. If it is not, an ValueError will be raised. Otherwise, Page.remove() will be called to remove the element of the page BTree.find() returned.
        If a DegreeUnderflowError is raised by Page.remove(), BTree.demote() will be called with the page that needed measures to be taken as a parameter.
        """
        arguments = merge_to_list(args)
        for arg in arguments:
            in_tree, page_pointer = self.find(arg)
            if in_tree == True:
                if len(page_pointer.descendent_pages) == 0:
                    try:
                        page_pointer.remove(arg)
                    except DegreeUnderflowError as e:
                        if self.can_borrow(e.page):
                            self.borrow(e.page)
                        else:
                            raise NotImplementedError()
                            # self.demote(e.page)
                else:
                    number = page_pointer.get_adjacent_element()
                    self.remove(number)
                    page_pointer.keys[page_pointer.index(arg)] = number
            else:
                raise ValueError("The value {} is not in this tree.".format(arg))

    def can_borrow(self, page, with_excedent_number=False):
        if with_excedent_number == True:
            return (self.can_borrow_left(page), self.can_borrow_right(page))
        else:
            return self.can_borrow_left(page)[0] or self.can_borrow_right(page)[0]

    def can_borrow_left(self, page):
        if not is_class(page, "RootPage"):
            parent_page = page.parent_page
            page_index = parent_page.descendent_pages.index(page)
            if page_index == 0:
                return (False, 0)
            else:
                left_sibling = parent_page.descendent_pages[page_index - 1]
                if len(left_sibling) > left_sibling.min_num_keys:
                    return (True, len(left_sibling) - left_sibling.min_num_keys)
                else:
                    return (False, 0)
        else:
            return (False, 0)

    def can_borrow_right(self, page):
        if not is_class(page, "RootPage"):
            parent_page = page.parent_page
            page_index = parent_page.descendent_pages.index(page)
            if page_index == len(parent_page) + 1:
                return (False, 0)
            else:
                right_sibling = parent_page.descendent_pages[page_index + 1]
                if len(right_sibling) > right_sibling.min_num_keys:
                    return (True, len(right_sibling) - right_sibling.min_num_keys)
                else:
                    return (False, 0)
        else:
            return (False, 0)

    def borrow(self, page):
        borrow_possibilities = self.can_borrow(page, True)
        parent_page = page.parent_page
        page_index = parent_page.descendent_pages.index(page)

        if borrow_possibilities[0][1] > borrow_possibilities[1][1]:
            print("[BTree.borrow()] Borrowing from the left page!")
            return self.borrow_left(page, parent_page, page_index)
        elif borrow_possibilities[1][1] > borrow_possibilities[0][1]:
            print("[BTree.borrow()] Borrowing from the right page!")
            return self.borrow_right(page, parent_page, page_index)
        else:
            raise Exception("Cannot borrow!")

    def borrow_left(self, page, parent_page, page_index):
        print("[BTree.borrow_left()] page: {}".format(page))
        print("[BTree.borrow_left()] parent_page: {}".format(parent_page))
        left_page = parent_page.descendent_pages[page_index - 1]
        print("[BTree.borrow_left()] left_page: {} (index {})".format(left_page, page_index - 1))
        element_to_borrow = left_page[-1]
        print("[BTree.borrow_left()] element_to_borrow: {}".format(element_to_borrow))
        middle_element = parent_page[page_index - 1]
        left_page.keys.remove(element_to_borrow)
        print("[BTree.borrow_left()] middle_element: {}".format(element_to_borrow))
        parent_page.keys[page_index - 1] = element_to_borrow
        insert_crescent(middle_element, page.keys)

    def borrow_right(self, page, parent_page, page_index):
        print("[BTree.borrow_left()] page: {}".format(page))
        print("[BTree.borrow_left()] parent_page: {}".format(parent_page))
        right_page = parent_page.descendent_pages[page_index + 1]
        print("[BTree.borrow_left()] right_page: {} (index {})".format(right_page, page_index + 1))
        element_to_borrow = right_page[0]
        print("[BTree.borrow_right()] element_to_borrow: {}".format(element_to_borrow))
        middle_element = parent_page[page_index]
        right_page.keys.remove(element_to_borrow)
        print("[BTree.borrow_right()] middle_element: {}".format(element_to_borrow))
        parent_page.keys[page_index] = element_to_borrow
        insert_crescent(middle_element, page.keys)
