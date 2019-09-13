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
tree.insert(63)
tree.insert(40)
# tree.insert(list(range(64,1000,1)))
# tree.insert(64,65,66,67,68,69,70,71,72,1,2,3,4,5,6,7,8,9,21,22,23,24,25,26,27,28,29,34,35,36,38,39,40,73,74,75,76,77,78,79,80,81)
# tree = BTree(
#    2, [3, 4, 8, 9, 10, 11, 13, 17, 20, 25, 28, 30, 33, 36, 40, 43, 45, 48, 50, 52, 55]
#)

