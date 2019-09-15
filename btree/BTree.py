# from btree.RootPage import *
from btree.helper import *
from btree.Page import *


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
        self.root = Page(min_num_keys, self, None)
        self.num_keys = 0

        self.insert(*args)

    def __contains__(self, element):
        return self.find(element)[0]

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
                in_tree, page_pointer, _ = self.find(arg)
                if in_tree:
                    raise ValueError("O valor {} já está na árvore.".format(arg))
                    continue
                try:
                    page_pointer.insert(arg)
                except DegreeOverflowError as e:
                    print("[BTree.insert()] DegreeOverflowError caught! Calling BTree.promote()...")
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
                return (True, page_pointer, page_pointer.index(element))
            else:
                new_page_pointer = page_pointer.get_probable_descendent(element)
                if new_page_pointer:
                    page_pointer = new_page_pointer
                else:
                    return (False, page_pointer, -1)

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

        for descendent in left_child.descendent_pages:
            descendent.parent_page = left_child
        for descendent in right_child.descendent_pages:
            descendent.parent_page = right_child

        for item in left_keys:
            left_child.insert(item)
        for item in right_keys:
            right_child.insert(item)

        if page.is_root():
            print("[BTree.promote()] Is RootPage! RootPage: {} Type: {}".format(page, type(page)))
            self.promote_root_page(page, left_child, middle_key, right_child)
        else:
            print("[BTree.promote()] Is Page! Page: {} Type: {}".format(page, type(page)))
            self.promote_page(page, left_child, middle_key, right_child)

    def promote_root_page(self, page, left_child, middle_key, right_child):
        page.keys = [middle_key]
        page.descendent_pages = [left_child, right_child]
        left_child.parent_page = page
        right_child.parent_page = page
        print("[BTree.promote_root_page()] Page: {}".format(page))

    def promote_page(self, page, left_child, middle_key, right_child):
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
            print("[BTree.promote_page()] DegreeOverflowError!")
            self.promote(parent_page)
        elif not parent_page.is_root() and len(parent_page) < parent_page.min_num_keys:
            print("[BTree.promote_page()] DegreeUnderflowError!")
            self.demote(parent_page)

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
            in_tree, page_pointer, arg_index = self.find(arg)
            if in_tree == True:
                if page_pointer.is_leaf():
                    print("[BTree.remove()] {} is leaf!".format(page_pointer))
                    try:
                        page_pointer.remove(arg)
                    except DegreeUnderflowError as e:
                        if e.page.can_borrow():
                            e.page.borrow()
                        else:
                            self.demote(e.page)
                else:
                    try:
                        print("[BTree.remove()] {} is not leaf!".format(page_pointer))
                        page_pointer.replace_with_leaf_element(arg)
                    except DegreeUnderflowError as e:
                        self.demote(e.page)
            else:
                raise ValueError("The value {} is not in this tree.".format(arg))
    
    def demote(self, page):
        parent_page = page.parent_page
        page_index = page.parent_page.descendent_pages.index(page)
        print("[BTree.demote()] page: {}".format(page))
        print("[BTree.demote()] parent_page: {}".format(parent_page))
        print("[BTree.demote()] page_index: {}".format(page_index))
        if page.get_left_page():
            print("[BTree.demote()] Calling BTree.demote_left()!")
            self.demote_left(page, page_index)
        else:
            print("[BTree.demote()] Calling BTree.demote_right()!")
            self.demote_right(page, page_index)
        
        if not parent_page.is_root() and len(parent_page) < parent_page.min_num_keys:
            print("[BTree.demote()] Page that would be demoted: {}".format(parent_page))
            print("[BTree.demote()] Page.parent_page: {}".format(parent_page.parent_page))
            self.demote(parent_page)
        
        elif parent_page.is_root() and len(parent_page) == 0:
            print("[BTree.demote()] RootPage is empty!")
            self.recreate_root()
        
    def demote_left(self, page, page_index):
        print("[BTree.demote_left()] page: {}".format(page))
        parent_page = page.parent_page
        print("[BTree.demote_left()] parent_page: {}".format(parent_page))
        left_page = page.get_left_page()
        middle_element = parent_page[page_index - 1]
        print("[BTree.demote_left()] left_page: {}".format(left_page))
        print("[BTree.demote_left()] middle_element: {}".format(middle_element))
        parent_page.remove(middle_element, will_raise = False)
        left_page.insert(middle_element, will_raise = False)
        for element in page:
            left_page.insert(element, will_raise = False)
        left_page.descendent_pages = left_page.descendent_pages + page.descendent_pages
        print("[BTree.demote_left()] Final page: {}".format(left_page))
        print("[BTree.demote_left()] Final page descendents: {}".format(left_page.descendent_pages))
        parent_page.descendent_pages.remove(page)
        
        left_page.update_descendents_parent_references()
        
        if len(left_page) > left_page.max_num_keys:
            print("[BTree.demote_left()] DegreeOverflowError!")
            self.promote(left_page)
    
    def demote_right(self, page, page_index):
        print("[BTree.demote_right()] page: {}".format(page))
        parent_page = page.parent_page
        print("[BTree.demote_right()] parent_page: {}".format(parent_page))
        right_page = page.get_right_page()
        middle_element = parent_page[page_index]
        print("[BTree.demote_right()] right_page: {}".format(right_page))
        print("[BTree.demote_right()] middle_element: {}".format(middle_element))
        parent_page.remove(middle_element, will_raise = False)
        right_page.insert(middle_element, will_raise = False)
        for element in page:
            right_page.insert(element, will_raise = False)
        right_page.descendent_pages = page.descendent_pages + right_page.descendent_pages
        print("[BTree.demote_right()] Final page: {}".format(right_page))
        print("[BTree.demote_right()] Final page descendents: {}".format(right_page.descendent_pages))
        parent_page.descendent_pages.remove(page)
        
        right_page.update_descendents_parent_references()
        
        if len(right_page) > right_page.max_num_keys:
            print("[BTree.demote_left()] DegreeOverflowError!")
            self.promote(right_page)
        
    def recreate_root(self):
        if len(self.root.descendent_pages) > 1:
            print("[BTree.recreate_root()] self.root: {}".format(self.root))
            print("[BTree.recreate_root()] self.root.descendent_pages: {}".format(self.root.descendent_pages))
            raise ValueError("There's more than a root?")
        self.root = self.root.descendent_pages[0]
        self.root.parent_page = None
        self.root.update_descendents_parent_references()
        
    def __repr__(self):
        height = self.get_height()
        representations = [" ".join([str(item) for item in self.get_pages_of_height(height)])]
        max_length = len(representations[0])
        
        for h in range(height - 1,0,-1):
            list_of_elements = self.get_pages_of_height(h)
            string_representation = " ".join([str(item) for item in self.get_pages_of_height(h)])
            list_length = len(list_of_elements)
            string_length = len(string_representation)
            number_of_spaces = int((max_length - string_length)/(list_length + 1))
            spaces = number_of_spaces * " "
            representation = spaces + spaces.join([str(item) for item in self.get_pages_of_height(h)]) + spaces
            representations.insert(0, representation)
        
        representations.insert(0, object.__repr__(self))
        
        return "\n".join(representations)
    
    def get_height(self):
        height = 1
        while self.get_pages_of_height(height + 1):
            height += 1
        return height
    
    def get_pages_of_height(self, height, merge_lists = True):
        try:
            pages = self.root.get_pages_of_height(height)
            if merge_lists:
                return merge_to_list_of_lists(pages)
            else:
                return pages
        except:
            return None