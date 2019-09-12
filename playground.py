from os import getcwd
from sys import path as sys_path

sys_path.append(getcwd())
from btree import *

# tree = BTree(2, [1, 7, 14, 20, 80])
# tree.insert(2,3,4)
tree = BTree(2, 20, 30, 37, 50)
tree.insert(42)
tree.insert(47, 41)
tree.insert(60)
tree.insert(31, 32, 43, 44, 61, 62)
tree.insert(33, 45)
# tree.insert(63)
# tree = BTree(
#    2, [3, 4, 8, 9, 10, 11, 13, 17, 20, 25, 28, 30, 33, 36, 40, 43, 45, 48, 50, 52, 55]
#)

