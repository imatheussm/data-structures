def handle_txt(file_name):
    try:
        with open(f"text_examples/{file_name}", 'r', encoding="utf-8") as file:
            return ''.join(file.readlines())

    except FileNotFoundError:
        raise FileNotFoundError(f"No such file or directory has been found: text_examples/{file_name}")


def handle_mask(pattern):
        mask = {char : ['0'] * len(pattern) for char in pattern}  

        for i in range(len(pattern)):
            mask[pattern[i]][i] = '1' 

        mask = {char : int(''.join(char_mask), 2) for char, char_mask in mask.items()}

        mask['*'] = 0

        return mask


def check_match(mask):
    return True if bin(mask)[-1] == '1' else False

