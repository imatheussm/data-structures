def handle_txt(file_name):
    try:
        with open(f"text_examples/{file_name}", 'r', encoding="utf-8") as file:
            return ''.join(file.readlines())
    except FileNotFoundError:
        raise FileNotFoundError(f"No such file or directory has been found: text_examples/{file_name}")