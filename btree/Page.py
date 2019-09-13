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
        if parent_page:
            self.parent_page = parent_page
        if parent_tree:
            self.parent_tree = parent_tree

    def __contains__(self, value):
        return value in self.keys

    def __repr__(self):
        return "[ " + " | ".join([(str(key)) for key in self.keys]) + " ]"

    def __len__(self):
        return len(self.keys)

    def __iter__(self):
        return iter(self.keys)

    def __getitem__(self, *args, **kwargs):
        return self.keys.__getitem__(*args, **kwargs)

    def insert(self, element, willRaise=True):
        """Inserts a number in the B-Tree."""
        insert_crescent(element, self.keys)
        self.num_keys += 1
        if willRaise and len(self.keys) > self.max_num_keys:
            raise DegreeOverflowError(self)

    def return_pointer(self, element):
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

    def remove(self, element):
        self.keys.remove(element)
        self.num_keys -= 1

        if not is_class(self, "RootPage") and len(self) < self.min_num_keys:
            raise DegreeUnderflowError(self)

    def index(self, *args, **kwargs):
        return self.keys.index(*args, **kwargs)

    def get_adjacent_element(self):
        previous_element, previous_page = self.get_previous_element(True)
        next_element, next_page = self.get_next_element(True)

        if len(next_page) > len(previous_page):
            return next_element
        else:
            return previous_element

    def get_previous_element(self, with_page=False):
        new_pointer = self.descendent_pages[0]

        while new_pointer:
            pointer = new_pointer
            try:
                new_pointer = pointer.descendent_pages[-1]
            except IndexError:
                if with_page:
                    return (pointer[-1], pointer)
                else:
                    return pointer[-1]

    def get_next_element(self, with_page=False):
        new_pointer = self.descendent_pages[-1]

        while new_pointer:
            pointer = new_pointer
            try:
                new_pointer = pointer.descendent_pages[0]
            except IndexError:
                if with_page:
                    return (pointer[0], pointer)
                else:
                    return pointer[0]

