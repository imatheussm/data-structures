def handle_txt(file_path):
    try:
        with open(f"text_examples/{file_path}", 'r') as file:
            return ''.join(file.readlines())
    except FileNotFoundError:
        raise FileNotFoundError(f"No such file or directory has been found: text_examples/{file_path}")