from os import getcwd
from sys import path as sys_path
sys_path.append(getcwd())
from btree import *

tree = BTree(4, [1,3,2,4,0,9,-3])