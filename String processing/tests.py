from os import getcwd
from sys import path as sys_path

import patternMatching
sys_path.append(getcwd())

c = patternMatching.ExactMatching("example.txt", "test")
print(c.new_brute_force())
print(c.new_BMH())
print(c.new_BMHS())

x = patternMatching.ExactMatching("example2.txt", "tooth")
print(x.new_BMH())

y = patternMatching.ExactMatching("example3.txt", "cade")
print(y.new_BMHS())

print("** ShiftAnd exato **")
print(c.ShiftAnd())
print(x.ShiftAnd())
print(y.ShiftAnd())

print("** ShiftAnd aproximado **")
a = patternMatching.FuzzyMatching("example4.txt", "teste")
print(a.ShiftAnd(1, True, False, False))
print(a.ShiftAnd(1, False, True, False))
print(a.ShiftAnd(1, False, False, True))
print(a.ShiftAnd(1, True, False, False)) 

