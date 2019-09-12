from btree.RootPage import *
from btree.helper import *
from btree.DegreeOverflowError import *

class BTree:
    """The B-Tree object per se."""

    def __init__(self, min_num_keys, *args):
        self.root = RootPage(min_num_keys, self)
        self.num_keys = 0
        
        elements_to_insert = merge_to_list(*args)
        for element in elements_to_insert:
            try:
                #self.insert(element) TO BE CREATED
                print("[BTree.__init__()] Argument: {}".format(element))
                self.insert(element)
            except DegreeOverflowError:
                pass
        del(elements_to_insert)

    def insert(self, *args):
        for arg in args:
            print("[BTree.insert()] Argument: {}".format(arg))
            if type(arg) in SUPPORTED_LIST_TYPES:
                for item in arg:
                    self.insert(arg)
                return
            elif type(arg) in SUPPORTED_TYPES:
                page_pointer = self.find(arg)
                if page_pointer[0] == True:
                    print("O valor {} já está na árvore.".format(arg))
                    return
                try:
                    page_pointer[1].insert(arg)
                except DegreeOverflowError as e:
                    self.promoteRoot(e.page)
            else:
                raise TypeError(
                    "This type is not supported. Type of the argumenet: {}".format(
                        str(type(arg))
                    )
                )
                
            self.num_keys += 1

    def promoteRoot(self, page):
        middle_index = int((len(page.keys) - 1) / 2)
        left_child = page.keys[:middle_index].copy()
        right_child = page.keys[middle_index + 1 :].copy()
        
        print("left_child: {}, right_child: {}".format(left_child, right_child))
        
        page.keys = [page.keys[middle_index]]
        page.descendent_pages[0] = Page(
            page.min_num_keys, page.parent_tree, page
        )
        for child in left_child:
            page.descendent_pages[0].insert(child)
        page.descendent_pages[1] = Page(
            page.min_num_keys, page.parent_tree, page
        )
        for child in right_child:
            page.descendent_pages[1].insert(child)

    def find(self,element):
        page_pointer = self.root
        
        while True:
            if element in page_pointer:
                return (True, page_pointer)
            else:
                new_page_pointer = page_pointer.return_pointer(element)
                if new_page_pointer: page_pointer = new_page_pointer
                else: 
                    return (False, page_pointer)