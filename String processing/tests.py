from os import getcwd
from sys import path as sys_path

import patternMatching
sys_path.append(getcwd())

c = patternMatching.ExactMatching("example.txt", "test")

print(c.new_brute_force())
c.new_BMH()
c.new_BMHS()

x = patternMatching.ExactMatching("example2.txt", "tooth")
x.BMH()

y = patternMatching.ExactMatching("example3.txt", "cade")
y.new_BMHS()