from os import getcwd
from sys import path as sys_path

import graphs

sys_path.append(getcwd())

# y = graphs.ListGraph(["bacon", "queijo", "arroz"], True, False)
# y = graphs.ListGraph(range(6), True, False)
# B = (("bacon", "arroz"), ("arroz", "queijo"))
# B = ((0, 1), (1, 2), (2, 3), (3, 1), (1, 4), (0, 4), (5, 0), (5, 4), (4, 3))

# y = graphs.ListGraph(range(1,7), False, False)
# B = ((6, 4), (4, 3), (4, 5), (5, 2), (2, 3), (5, 1), (2, 1))

# y = graphs.MatrixGraph(range(10), True, False)
# B = ((0, 3), (0, 2), (0, 1), (0, 5), (1, 2), (2, 3), (2, 4), (4, 6), (5, 4), (5, 6), (6, 7), (6, 8), (7, 8), (9, 6))

# y = graphs.ListGraph(list(range(1, 7)), True, False)
# B = ((1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6))

# y = graphs.MatrixGraph(list(range(6)), False, False)
# B = ((0, 1), (0, 3), (1, 2), (1, 3), (2, 3), (4, 5))

# y = graphs.MatrixGraph(list(range(1, 7)), False, False)
# B = ((1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 5), (4, 6), (5, 6))

# y = graphs.ListGraph(list(range(6)), True, True)
# B = ((0, 1), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3), (3, 0), (5, 4))

# y = graphs.ListGraph(list(range(4)), True, False)
# B = ((0, 1), (0, 3), (1, 2), (2, 0), (2, 3))

# y = graphs.MatrixGraph(list(range(6)), False, True)
# B = ((0, 1, 6), (0, 2, 1), (0, 3, 5),
#      (1, 2, 2), (1, 4, 5),
#      (2, 3, 2), (2, 4, 6), (2, 5, 4),
#      (3, 5, 4),
#      (4, 5, 3))

# y = graphs.MatrixGraph(list(range(5)), True, True)
# B = ((0, 1, 1), (0, 3, 3), (0, 4, 10),
#      (1, 2, 5),
#      (2, 4, 1),
#      (3, 2, 2), (3, 4, 6))

# y = graphs.MatrixGraph(["Home", "A", "B", "C", "D", "E", "F", "School"], False, True)
# B = (("Home", "A", 3), ("Home", "B", 2), ("Home", "C", 5),
#      ("A", "D", 3),
#      ("B", "D", 1), ("B", "E", 6),
#      ("C", "E", 2),
#      ("D", "F", 4),
#      ("E", "F", 1), ("E", "School", 4),
#      ("F", "School", 2))

# y = graphs.ListGraph(["S", "A", "B", "C", "D", "E", "F"], True, True)
# B = (("S", "A", 3), ("S", "C", 2), ("S", "F", 6),
#      ("A", "B", 6), ("A", "D", 1),
#      ("B", "E", 1),
#      ("C", "D", 3),
#      ("D", "E", 4),
#      ("F", "E", 2))

# y = graphs.MatrixGraph(["A", "B", "C", "D", "E", "F", "G", "H"], False, True)
# B = (("A", "B", 8), ("A", "C", 2), ("A", "D", 5),
#      ("B", "D", 2), ("B", "F", 13),
#      ("C", "D", 2), ("C", "E", 5),
#      ("D", "E", 1), ("D", "F", 6), ("D", "G", 3),
#      ("E", "G", 1),
#      ("F", "G", 2), ("F", "H", 3),
#      ("G", "H", 6))

# y = graphs.ListGraph(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "z"], False, True)
# B = (("a", "b", 3), ("a", "e", 5), ("a", "h", 4),
#      ("b", "c", 2), ("b", "e", 5), ("b", "f", 7),
#      ("c", "d", 3), ("c", "f", 2), ("c", "g", 6),
#      ("d", "g", 7), ("d", "z", 2),
#      ("e", "f", 4), ("e", "h", 7),
#      ("f", "g", 4), ("f", "h", 5), ("f", "i", 4), ("f", "j", 3),
#      ("g", "j", 4), ("g", "z", 6),
#      ("h", "i", 2),
#      ("i", "j", 6),
#      ("j", "z", 5))

# y = graphs.ListGraph(list(range(1, 7)), True, True)
# B = (
#     (1, 2, 15),
#     (1, 3, 9),
#     (2, 4, 2),
#     (3, 2, 4),
#     (3, 4, 3),
#     (3, 5, 16),
#     (4, 5, 6),
#     (4, 6, 21),
#     (5, 6, 7),
# )

# y = graphs.MatrixGraph(["A", "B", "C", "D", "E", "F", "G", "H", "I"], False, True)
# B = (
#     ("A", "B", 12), ("A", "C", 22), ("A", "D", 15), ("A", "G", 25),
#     ("B", "C", 8), ("B", "E", 16),
#     ("C", "F", 17), ("C", "I", 40),
#     ("D", "E", 15), ("D", "G", 14),
#     ("E", "F", 10), ("E", "H", 16),
#     ("F", "I", 18),
#     ("G", "H", 13), ("G", "I", 21),
#     ("H", "I", 11)
#
# )

y = graphs.ListGraph(["A", "B", "C", "D", "E", "F", "G"], False, False)
B = (
    ("A", "B"), ("A", "C"),
    ("B", "D"),
    ("C", "D"), ("C", "E"), ("C", "G"),
    ("D", "E"),
    ("E", "F")
)

for edge in B:
    y.add_edge(*edge)
