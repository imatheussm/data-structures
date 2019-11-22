from patternMatching import Matching
from patternMatching.helpers import handle_mask, check_match


class ExactMatching(Matching):
    def __init__(self, file_path, pattern=None):
        super().__init__(file_path, pattern)

    def new_brute_force(self):
        occurrences = []

        for s in range(self.n - self.m + 1):
            if self.pattern == self.text[s:s + self.m]: occurrences.append((s, s + self.m - 1))

        return tuple(occurrences)

    def brute_force(self):  # normal algorithm, comparing char by char. similar to ziviani's implementation
        occurrences = []

        for s in range(self.n - self.m + 1):
            k, j = s, 0

            while j < self.m and self.text[k] == self.pattern[j]:
                j += 1
                k += 1

            if j == self.m: occurrences.append((s, s + self.m - 1))

        return tuple(occurrences)

    def new_BMH(self):
        occurrences = []

        table = {item: self.m - index - 1 for index, item in enumerate(self.pattern[:self.m - 1])}

        # If the last pattern character is not already in the table, the default value (pattern length) is defined for it. If not, it keeps with the same value. 
        table[self.pattern[self.m - 1]] = self.m if self.pattern[self.m - 1] not in table.keys() else table[self.pattern[self.m - 1]]

        # The default value (pattern length) is defined for all the other characters (represented by *) that are not being used in the pattern.
        table['*'] = self.m 
                                                                      
        # print(table)                                                  
                                                                      
        i, p = self.m - 1, 0

        while i < self.n:
            # print(f"Pattern: {self.pattern} Text: {self.text[p:i+1]}")
            if self.pattern == self.text[p:i + 1]: occurrences.append((p, p + self.m - 1))

            char = self.text[i] if self.text[i] in self.pattern else '*'

            p += table[char]
            i += table[char]
        
        return tuple(occurrences)

    def BMH(self):  # similar to ziviani's implementation with some adjustments
        occurrences = []

        table = {item: self.m - index - 1 for index, item in enumerate(self.pattern[:self.m - 1])}

        table[self.pattern[self.m - 1]] = self.m if self.pattern[self.m - 1] not in table.keys() else table[self.pattern[self.m - 1]]
        
        table['*'] = self.m

        i = self.m - 1

        while i < self.n:
            k, j = i, self.m - 1

            while j >= 0 and self.text[k] == self.pattern[j]:
                j -= 1
                k -= 1

            if j < 0: occurrences.append((k + 1, k + self.m))
                # print(f"Pattern matching occurred at position {k + 1}")

            i += table[self.text[i] if self.text[i] in self.pattern else '*']
        
        return tuple(occurrences)

    def new_BMHS(self):
        occurrences = []

        table = {item: self.m - index for index, item in enumerate(self.pattern)}

        table['*'] = self.m + 1

        # print(table)

        i, p = self.m - 1, 0

        while i < self.n:
            # print(f"Pattern: {self.pattern} Text: {self.text[p:i + 1]}")

            if self.pattern == self.text[p:i + 1]: occurrences.append((p, p + self.m - 1))
                #print(f"Pattern matching occurred at position {p}")

            try:
                char = self.text[i + 1] if self.text[i + 1] in self.pattern else '*'
            except:
                break

            p += table[char]
            i += table[char]

        return tuple(occurrences)

    def BMHS(self):  # similar to ziviani's implementation with some adjustments
        occurrences = []

        table = {item: self.m - index for index, item in enumerate(self.pattern)}

        table['*'] = self.m + 1

        # print(table)

        i = self.m - 1

        while i < self.n:
            k, j = i, self.m - 1

            while j >= 0 and self.text[k] == self.pattern[j]:
                j -= 1
                k -= 1

            if j < 0:
                occurrences.append((k + 1, k + self.m))

            try:
                char = self.text[i + 1] if self.text[i + 1] in self.pattern else '*'
            except:
                break

            i += table[char]

        return tuple(occurrences)

    def ShiftAnd(self):
        occurrences = []
        
        mask = handle_mask(self.pattern)

        R = 0

        for i in range(self.n):
            char = self.text[i] if self.text[i] in mask.keys() else '*' 

            R = (R >> 1 | self.fixed_mask) & mask[char]

            if check_match(R): occurrences.append((i - self.m + 1, i))
        
        return tuple(occurrences)
