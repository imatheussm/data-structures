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

y = graphs.MatrixGraph(range(10), True, False)
B = ((0, 3), (0, 2), (0, 1), (0, 5), (1, 2), (2, 3), (2, 4), (4, 6), (5, 4), (5, 6), (6, 7), (6, 8), (7, 8), (9, 6))


for (origin, destination) in B:
    y.add_edge(origin, destination)