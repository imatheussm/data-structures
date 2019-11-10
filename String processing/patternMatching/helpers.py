def handle_txt(file_path):
    try:
        file = open(f"text_examples/{file_path}", "r")
        txt = ''.join(file.readlines())
        return txt
    except:
        raise FileExistsError(f"{file_path} file doesn't exist.")