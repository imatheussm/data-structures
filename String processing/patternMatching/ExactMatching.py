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
        table[self.pattern[self.m - 1]], table['*'] = self.m, self.m  # Adding default values to the last pattern
                                                                      # character and to all the other characters (
        print(table)                                                  # represented by *) that are not being used in the
                                                                      # pattern.
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
        table[self.pattern[self.m - 1]], table['*'] = self.m, self.m

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
            print(f"Pattern: {self.pattern} Text: {self.text[p:i + 1]}")

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
