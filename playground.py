from os import getcwd
from sys import path as sys_path

sys_path.append(getcwd())
from btree import *

# tree = BTree(2, [1, 3, 2, 4, 5])
tree = BTree(
    2, [3, 4, 8, 9, 10, 11, 13, 17, 20, 25, 28, 30, 33, 36, 40, 43, 45, 48, 50, 52, 55]
)

