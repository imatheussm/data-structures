from btree.helper import *
from btree.constants import *
from btree.DegreeOverflowError import *
from btree.DegreeUnderflowError import *


class Page:
    """A Page of the B-Tree.
    
    This page is inherited by RootPage and LeafPage classes.
    """

    def __init__(self, min_num_keys, parent_tree, parent_page):
        # self.depth = 0
        # self.height = 1
        # self.level = self.depth + 1
        self.descendent_pages = []
        self.keys = []
        self.max_num_keys = 2 * min_num_keys
        self.min_num_keys = min_num_keys
        self.num_keys = 0
        self.parent_page = parent_page
        if parent_tree:
            self.parent_tree = parent_tree

    def __contains__(self, value):
        return value in self.keys

    def __repr__(self, compact = False):
        if compact:
            return "[" + "|".join([(str(key)) for key in self.keys]) + "]"
        else:
            return "[ " + " | ".join([(str(key)) for key in self.keys]) + " ]"

    def __len__(self):
        return len(self.keys)

    def __iter__(self):
        return iter(self.keys)

    def __getitem__(self, *args, **kwargs):
        return self.keys.__getitem__(*args, **kwargs)

    def insert(self, element, will_raise=True):
        """Inserts a number in the B-Tree."""
        insert_crescent(element, self.keys)
        self.num_keys += 1
        if will_raise and len(self.keys) > self.max_num_keys:
            print("[Page.insert()] Raising DegreeOverflowError!")
            raise DegreeOverflowError(self)

    def get_probable_descendent(self, element):
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

    def find(self, element):
        try:
            return self.keys.index(element)
        except ValueError:
            return None

    def remove(self, element, will_raise = True):
        self.keys.remove(element)
        self.num_keys -= 1

        if self.parent_page != None and len(self) < self.min_num_keys:
            raise DegreeUnderflowError(self)

    def index(self, *args, **kwargs):
        return self.keys.index(*args, **kwargs)

    def get_adjacent_element(self, number, with_page = False):
        previous_element, previous_page = self.get_previous_element(number, True)
        next_element, next_page = self.get_next_element(number, True)

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

    def get_previous_element(self, number, with_page=False):
        index = self.index(number)
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

    def get_next_element(self, number, with_page=False):
        index = self.index(number)
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
        return (get_left_page(self), get_right_page(self))

    def get_left_page(self):
        if self.parent_page == None:
            return None
        else:
            page_pointer_index = self.parent_page.descendent_pages.index(self)
            if page_pointer_index == 0:
                return None
            else:
                return self.parent_page.descendent_pages[page_pointer_index - 1]
    
    def get_right_page(self):
        if self.parent_page == None:
            return None
        else:
            page_pointer_index = self.parent_page.descendent_pages.index(self)
            if page_pointer_index == len(self.parent_page):
                return None
            else:
                return self.parent_page.descendent_pages[page_pointer_index + 1]

    def can_get_borrowed(self):
        if self.is_leaf():
            return len(self) - self.min_num_keys
        else:
            return 0

    def can_borrow(self, with_excedent_number=False):
        if with_excedent_number == True:
            return (self.can_borrow_left(), self.can_borrow_right())
        else:
            return bool(self.can_borrow_left() or self.can_borrow_right())
    
    def can_borrow_left(self):
        try:
            return self.get_left_page().can_get_borrowed()
        except:
            return 0
        
    def can_borrow_right(self):
        try:
            return self.get_right_page().can_get_borrowed()
        except:
            return 0
        
    def borrow(self):
        borrow_possibilities = self.can_borrow(True)

        if borrow_possibilities[0] > borrow_possibilities[1]:
            print("[BTree.borrow()] Borrowing from the left page!")
            return self.borrow_left()
        elif borrow_possibilities[1] > borrow_possibilities[0]:
            print("[BTree.borrow()] Borrowing from the right page!")
            return self.borrow_right()
        elif borrow_possibilities[0] > 0:
            print("[BTree.borrow()] Borrowing from the left page!")
            return self.borrow_left()
        else:
            raise Exception("Cannot borrow!")
        
    def borrow_left(self):
        page_index = self.parent_page.descendent_pages.index(self)
        print("[BTree.borrow_left()] page: {}".format(self))
        print("[BTree.borrow_left()] parent_page: {}".format(self.parent_page))
        left_page = self.get_left_page()
        print("[BTree.borrow_left()] left_page: {} (index {})".format(left_page, page_index - 1))
        element_to_borrow = left_page[-1]
        print("[BTree.borrow_left()] element_to_borrow: {}".format(element_to_borrow))
        middle_element = self.parent_page[page_index - 1]
        left_page.keys.remove(element_to_borrow)
        print("[BTree.borrow_left()] middle_element: {}".format(element_to_borrow))
        self.parent_page.keys[page_index - 1] = element_to_borrow
        self.insert(middle_element)

    def borrow_right(self):
        page_index = self.parent_page.descendent_pages.index(self)
        print("[BTree.borrow_left()] page: {}".format(self))
        print("[BTree.borrow_left()] parent_page: {}".format(self.parent_page))
        right_page = self.get_right_page()
        print("[BTree.borrow_left()] right_page: {} (index {})".format(right_page, page_index + 1))
        element_to_borrow = right_page[0]
        print("[BTree.borrow_right()] element_to_borrow: {}".format(element_to_borrow))
        middle_element = self.parent_page[page_index]
        right_page.keys.remove(element_to_borrow)
        print("[BTree.borrow_right()] middle_element: {}".format(element_to_borrow))
        self.parent_page.keys[page_index] = element_to_borrow
        self.insert(middle_element)
        
    def get_pages_of_height(self, height, current_pointer = None, current_height = 1):
        pages = []
        
        if not current_pointer:
            current_pointer = self
        
        if current_height < height:
            if len(current_pointer.descendent_pages) > 0:
                for descendent in current_pointer.descendent_pages:
                    pages.append(self.get_pages_of_height(height, descendent, current_height + 1))
                return pages
            else:
                raise ValueError("The tree is not that tall!")
        else:
            return current_pointer.keys
        
    def is_leaf(self):
        return self.descendent_pages == []
    
    def is_root(self):
        return self.parent_page == None
    
    def replace_with_leaf_element(self, element):
        number, number_page = self.get_adjacent_element(element, with_page = True)
        print("[BTree.remove()] Adjacent element: {}, in page {}".format(number, number_page))
        number_page.keys.remove(number)
        self.keys[self.index(element)] = number
        
        self.update_descendents_parent_references()
        
        if len(number_page) < number_page.min_num_keys:
            raise DegreeUnderflowError(number_page)
        
    def update_descendents_parent_references(self):
        for descendent in self.descendent_pages:
            descendent.parent_page = self