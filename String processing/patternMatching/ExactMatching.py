from patternMatching import Matching

class ExactMatching(Matching):
    def __init__(self, file_path, pattern=None):
        super().__init__(file_path, pattern)

    def new_brute_force(self):
        n = len(self.text)
        m = len(self.pattern)

        for s in range(n-m+1):
            # print(f"Pattern: {self.pattern} Text: {self.text[s:s+m]}")
            if self.pattern == self.text[s:s+m]:
                print(f"Pattern matching occurred at position {s}")

    def brute_force(self): # normal algorithm, comparing char by char. similar to ziviani's implementation
        n = len(self.text)
        m = len(self.pattern)

        for s in range (n-m+1):
            k = s
            j = 0
            while j < m and self.text[k] == self.pattern[j]:
                j += 1
                k += 1
            if j == m:
                print(f"Pattern matching occurred at position {s}")
    
    def new_BMH(self):
        n = len(self.text)
        m = len(self.pattern)
        
        table = {item: m-index-1 for index, item in enumerate(self.pattern[:m-1])}
        table[self.pattern[m-1]], table['*'] = m, m # Adding default values to the last pattern character and to all the other characters (represented by *) that are not being used in the pattern.
        print(table)

        i = m-1
        p = 0

        while (i < n):
            # print(f"Pattern: {self.pattern} Text: {self.text[p:i+1]}")
            if self.pattern == self.text[p:i+1]:
                print(f"Pattern matching occurred at position {p}")

            char = self.text[i] if self.text[i] in self.pattern else '*'

            p += table[char]
            i += table[char]

    def BMH(self): # similar to ziviani's implementation with some adjustments
        n = len(self.text)
        m = len(self.pattern)
        
        table = {item: m-index-1 for index, item in enumerate(self.pattern[:m-1])}
        table[self.pattern[m-1]], table['*'] = m, m
        
        i = m - 1

        while (i < n):
            k = i
            j = m-1

            while j >= 0 and self.text[k] == self.pattern[j]:
                j-=1
                k -=1
            
            if j < 0:
                print(f"Pattern matching occurred at position {k+1}")

            i += table[self.text[i] if self.text[i] in self.pattern else '*']

    def new_BMHS(self): 
        n = len(self.text)
        m = len(self.pattern)
        
        table = {item: m-index for index, item in enumerate(self.pattern)}
        table['*'] = m+1
        print(table)

        i = m-1
        p = 0

        while (i < n):
            print(f"Pattern: {self.pattern} Text: {self.text[p:i+1]}")
            if self.pattern == self.text[p:i+1]:
                print(f"Pattern matching occurred at position {p}")

            try:
                char = self.text[i+1] if self.text[i+1] in self.pattern else '*'
            except:
                break

            p += table[char]
            i += table[char]

    def BMHS(self): # similar to ziviani's implementation with some adjustments
        n = len(self.text)
        m = len(self.pattern)
        
        table = {item: m-index for index, item in enumerate(self.pattern)}
        table['*'] = m+1
        print(table)
        
        i = m - 1

        while (i < n):
            k = i
            j = m-1

            while j >= 0 and self.text[k] == self.pattern[j]:
                j-=1
                k -=1
            
            if j < 0:
                print(f"Pattern matching occurred at {k+1}")

            try:
                char = self.text[i+1] if self.text[i+1] in self.pattern else '*'
            except:
                break

            i += table[char]
