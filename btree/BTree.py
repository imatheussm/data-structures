from btree.RootPage import *
from btree.helper import *
from btree.DegreeOverflowError import *


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

        print("[BTree.__init__()] *args: {}".format(*args))
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

    def promote(self, page):
        """Promotes a number one level above.
        
        Parameters
        ----------
        self: BTree
            A BTree object.
        page: Page
            A Page object containing the elements to be treated.
        """
        middle_index = page.min_num_keys  # int((len(page.keys) - 1) / 2)
        left_keys = page[:middle_index].copy()
        middle_key = page[middle_index]
        right_keys = page[middle_index + 1 :].copy()

        print("[BTree.promote()] left_keys: {}".format(left_keys))
        print("[BTree.promote()] middle_key: {}".format(middle_key))
        print("[BTree.promote()] right_keys: {}".format(right_keys))

        if not is_class(page, "RootPage"):
            print("[BTree.promote()] Not RootPage!")
            parent_page = page.parent_page
            descendent_pages = page.descendent_pages

            insert_crescent(middle_key, parent_page.keys)
            insertion_index = parent_page.index(middle_key)

            left_child = Page(page.min_num_keys, self, parent_page)
            for element in left_keys:
                insert_crescent(element, left_child.keys)
            left_child.descendent_pages = descendent_pages[:len(left_child)]

            right_child = Page(page.min_num_keys, self, parent_page)
            for element in right_keys:
                insert_crescent(element, right_child.keys)
            right_child.descendent_pages = descendent_pages[len(left_child) + 1 :]

            parent_page.descendent_pages.insert(insertion_index, left_child)
            parent_page.descendent_pages.insert(insertion_index + 1, right_child)
            # for child in right_keys:
            #     insert_crescent(child, parent_page.descendent_pages[insertion_index + 1].keys)
            parent_page.descendent_pages.remove(page)
            
            if len(parent_page) > parent_page.max_num_keys:
                self.promote(parent_page)
        else:
            print("[BTree.promote()] Is RootPage!")
            descendent_pages = page.descendent_pages
            
            left_child = Page(page.min_num_keys, self, page)
            for element in left_keys:
                insert_crescent(element, left_child.keys)
            try:
                left_child.descendent_pages = page.descendent_pages[:middle_index + 1]
            except:
                pass
            right_child = Page(page.min_num_keys, self, page)
            for element in right_keys:
                insert_crescent(element, right_child.keys)
            try:
                right_child.descendent_pages = page.descendent_pages[middle_index + 1 :]
            except:
                pass

            page.keys = [middle_key]
            page.descendent_pages = [left_child, right_child]

    def demote(self, page):
        pass

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
                try:
                    page_pointer.remove(arg)
                except DegreeUnderflowError as e:
                    raise NotImplementedError()
            else:
                raise ValueError("The value {} is not in this tree.".format(arg))
