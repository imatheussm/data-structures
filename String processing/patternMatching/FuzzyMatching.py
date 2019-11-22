from patternMatching import Matching
from patternMatching.helpers import handle_mask, checkMatch

class FuzzyMatching(Matching):
    def __init__(self, file_path, pattern=None):
        super().__init__(file_path, pattern)

    def ShiftAnd(self, k, insertion=True, substitution=True, removal=True):
        occurrences = {'i': [], 's': [], 'r' : [], 'e' : []}

        mask = handle_mask(self.pattern)
        
        # print(f"Mask: {mask}")

        R = []

        for i in range(k+1):
            R.append(int(''.join(['1' * i + '0' * (self.m - i)]), 2))
            # print(f"R[{i}]: {R[i]}")

        for i in range(self.n):
            char = self.text[i] if self.text[i] in mask.keys() else '*'

            old_R = R[0]

            new_R = (old_R >> 1 | self.fixedMask) & mask[char]

            R[0] = new_R
            # print(f"R[0] na iteração {i}: {R[0]}")

            if checkMatch(R[0]): occurrences['e'].append((i - self.m + 1, i))

            for j in range(1, k+1):
                aux_R = new_R

                new_R = ((R[j] >> 1) & mask[char]) 

                if insertion:
                    new_R |= old_R

                    if checkMatch(new_R): occurrences['i'].append((i - self.m + 1 - j, i))
                    # print(f"Inserção que começa na posição {i - self.m + 1 - j} e termina em {i}!")
                
                if substitution:
                    new_R |= (old_R >> 1)

                    if checkMatch(new_R): occurrences['s'].append((i - self.m + 1, i))
                    # print(f"Substituição que começa na posição {i - self.m + 1} e termina em {i}!")

                if removal:
                    new_R |= (aux_R >> 1)

                    if checkMatch(new_R): occurrences['r'].append((i - self.m + 1 + j, i))
                    # print(f"Remoção que começa na posição {i - self.m + 1 + j} e termina em {i}!")

                old_R = R[j]

                R[j] = new_R | self.fixedMask

        return occurrences