from patternMatching import Matching


class FuzzyMatching(Matching):
    def __init__(self, file_path, pattern=None):
        super().__init__(file_path, pattern)

    def ShiftAnd(self, k):
        mask = {char: ['0'] * self.m for char in self.pattern}

        for i in range(self.m):
            mask[self.pattern[i]][i] = '1'

        for char in mask:
            mask[char] = int(''.join(mask[char]), 2)

        mask['*'] = 0

        print("Mask:", mask)

        R = []

        for i in range(k+1):
            R.append(['1' * i + '0' * (self.m - i)])
            print(f"R[{i}]: {R[i]}")
            R[i] = int(''.join(R[i]), 2)

        for i in range(self.n):
            char = self.text[i] if self.text[i] in mask.keys() else '*'

            old_R = R[0]

            new_R = ((old_R >> 1) | int('1' + '0' * (self.m - 1), 2)) & mask[char]

            R[0] = new_R
            print(f"R[0] na iteração {i}: {R[0]}")

            if bin(R[0])[-1] == '1':
                print(f"Exact pattern matching occurred at position {i - self.m + 1} ending at {i}")

            for j in range(1, k+1):
                new_R = ((R[j] >> 1) & mask[char]) | old_R | ((old_R | new_R) >> 1)

                old_R = R[j]

                R[j] = new_R | int('1' + '0' * (self.m - 1), 2)

                print(f"R[{j}] na iteração {i}: {R[j]}")

                if bin(R[j])[-1] == '1':
                    print(f"Fuzzy pattern matching occurred at position {i}")