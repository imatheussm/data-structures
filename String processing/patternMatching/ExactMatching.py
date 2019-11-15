from patternMatching import Matching

class ExactMatching(Matching):
    def __init__(self, file_path, pattern=None):
        super().__init__(file_path, pattern)

    def new_brute_force(self):
        occurrences = []

        for s in range(self.n - self.m + 1):
            print(f"Pattern: {self.pattern} | Text: {self.text[s:s + self.m]}", end="")

            if self.pattern == self.text[s:s + self.m]:
                occurrences.append((s, s + self.m))
                print(" <-")
            else:
                print()

        return tuple(occurrences)

    def brute_force(self):  # normal algorithm, comparing char by char. similar to ziviani's implementation
        occurrences = []

        for s in range(self.n - self.m + 1):
            k, j = s, 0

            print(f"Pattern: {self.pattern} | Text: {self.text[s:s + self.m]}", end="")

            while j < self.m and self.text[k] == self.pattern[j]:
                j += 1
                k += 1

            if j == self.m:
                occurrences.append((s, s + self.m))
                print(f" <-")
            else:
                print()

        return tuple(occurrences)

    def new_BMH(self):
        table = {item: self.m - index - 1 for index, item in enumerate(self.pattern[:self.m - 1])}

        # If the last pattern character is not already in the table, the default value (pattern length) is defined for it. If not, it keeps with the same value. 
        table[self.pattern[self.m - 1]] = self.m if self.pattern[self.m - 1] not in table.keys() else table[self.pattern[self.m - 1]]

        # The default value (pattern length) is defined for all the other characters (represented by *) that are not being used in the pattern.
        table['*'] = self.m 
                                                                      
        print(table)                                                  
                                                                      
        i, p = self.m - 1, 0

        while i < self.n:
            # print(f"Pattern: {self.pattern} Text: {self.text[p:i+1]}")
            if self.pattern == self.text[p:i + 1]:
                print(f"Pattern matching occurred at position {p}")

            char = self.text[i] if self.text[i] in self.pattern else '*'

            p += table[char]
            i += table[char]

    def BMH(self):  # similar to ziviani's implementation with some adjustments
        table = {item: self.m - index - 1 for index, item in enumerate(self.pattern[:self.m - 1])}

        table[self.pattern[self.m - 1]] = self.m if self.pattern[self.m - 1] not in table.keys() else table[self.pattern[self.m - 1]]
        
        table['*'] = self.m

        i = self.m - 1

        while i < self.n:
            k, j = i, self.m - 1

            while j >= 0 and self.text[k] == self.pattern[j]:
                j -= 1
                k -= 1

            if j < 0:
                print(f"Pattern matching occurred at position {k + 1}")

            i += table[self.text[i] if self.text[i] in self.pattern else '*']

    def new_BMHS(self):
        table = {item: self.m - index for index, item in enumerate(self.pattern)}
        table['*'] = self.m + 1
        print(table)

        i, p = self.m - 1, 0

        while i < self.n:
            # print(f"Pattern: {self.pattern} Text: {self.text[p:i + 1]}")

            if self.pattern == self.text[p:i + 1]:
                print(f"Pattern matching occurred at position {p}")

            try:
                char = self.text[i + 1] if self.text[i + 1] in self.pattern else '*'
            except:
                break

            p += table[char]
            i += table[char]

    def BMHS(self):  # similar to ziviani's implementation with some adjustments
        table = {item: self.m - index for index, item in enumerate(self.pattern)}
        table['*'] = self.m + 1
        print(table)

        i = self.m - 1

        while i < self.n:
            k, j = i, self.m - 1

            while j >= 0 and self.text[k] == self.pattern[j]:
                j -= 1
                k -= 1

            if j < 0:
                print(f"Pattern matching occurred at {k + 1}")

            try:
                char = self.text[i + 1] if self.text[i + 1] in self.pattern else '*'
            except:
                break

            i += table[char]

    def ShiftAnd(self):
        # Initializes the mask of each pattern character with a sequence of 0
        mask = {char : ['0'] * self.m for char in self.pattern}  

        # For each character's position in the pattern, put 1 in the corresponding position in the character's mask.
        for i in range(self.m):
            mask[self.pattern[i]][i] = '1' 

        R = 0

        # Converting each mask to string then to integer (to make bitwise operations possible)
        for char in mask:
            mask[char] = int(''.join(mask[char]), 2)

        # Initializes the mask of all the other characters (represented by *) that are not being used in the pattern
        mask['*'] = 0

        print(f"Mask: {mask}") # Mask with decimal values!

        for i in range(self.n):
            char = self.text[i] if self.text[i] in mask.keys() else '*' 

            R = (R >> 1 | int('1' + '0' * (self.m-1), 2)) & mask[char]

            if list(bin(R))[-1] == '1': # Checking if the last element of R is equals to 1. 
                print(f"Pattern matching occurred at position {i - self.m + 1}")