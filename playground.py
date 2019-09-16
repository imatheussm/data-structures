from os import getcwd
from sys import path as sys_path
from random import shuffle

sys_path.append(getcwd())
from btree import *


# tree = BTree(2, [1, 7, 14, 20, 80])
# tree.insert(2, 3, 4)
tree = BTree(2, 20, 30, 37, 50)
tree.insert(42)
tree.insert(47, 41)
tree.insert(60)
tree.insert(31, 32, 43, 44, 61, 62)
tree.insert(33, 45)
tree.insert(63)
tree.insert(64, 65)

# tree.insert(64, 65, 66, 67, 68, 69, 70, 71, 72)
# tree.insert(40)

# for degree in range(1, 11):
#     print("Current degree: {}...".format(degree))
#     to_add = list(range(1, 1000))
#     to_find = list(range(1, 1000))
#     to_remove = list(range(1, 1000))
#     shuffle(to_add)
#     shuffle(to_find)
#     shuffle(to_remove)

#     tree = BTree(degree, to_add)

#     for i in to_find:
#         in_tree, page_pointer, page_index = tree.find(i)
#         if not in_tree:
#             raise Exception("{} not found!".format(i))

#     for i in range(len(to_remove)):
#         if True:
#             # print("Removing {}...".format(to_remove[i]))
#             tree.remove(to_remove[i])
#             for i in to_remove[i + 1 :]:
#                 in_tree, page_pointer, page_index = tree.find(i)
#                 if not in_tree:
#                     raise Exception("{} not found!".format(i))
#         else:
#             break

# to_add = list(range(1, 100000))
# to_remove = list(range(1, 10000))
# to_find = list(range(1, 10000))
# shuffle(to_add)
# shuffle(to_remove)
# shuffle(to_find)

# tree = BTree(2, to_add)

# for index, item in enumerate(to_find):
#     print("Finding {}...".format(item), end="")
#     in_tree, page, page_index = tree.find(item)
#     if not in_tree:
#         raise Exception(
#             "Element not in tree! Element: {}. Index: {}.".format(item, index)
#         )
#     else:
#         print(" found!")

# tree = BTree(
#     2,
#     [
#         9,
#         28,
#         3,
#         6,
#         13,
#         16,
#         19,
#         22,
#         33,
#         1,
#         2,
#         4,
#         5,
#         7,
#         8,
#         11,
#         12,
#         14,
#         15,
#         17,
#         18,
#         20,
#         21,
#         23,
#         24,
#         26,
#         31,
#         32,
#         34,
#         35,
#     ],
# )
# tree.insert(list(range(64, 1000000, 1)))
# tree.insert(
#     64,
#     65,
#     66,
#     67,
#     68,
#     69,
#     70,
#     71,
#     72,
#     1,
#     2,
#     3,
#     4,
#     5,
#     6,
#     7,
#     8,
#     9,
#     21,
#     22,
#     23,
#     24,
#     25,
#     26,
#     27,
#     28,
#     29,
#     34,
#     35,
#     36,
#     38,
#     39,
#     40,
#     73,
#     74,
#     75,
#     76,
#     77,
#     78,
#     79,
#     80,
#     81,
# )
# tree = BTree(
#     2, [3, 4, 8, 9, 10, 11, 13, 17, 20, 25, 28, 30, 33, 36, 40, 43, 45, 48, 50, 52, 55]
# )

