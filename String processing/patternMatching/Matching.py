from patternMatching import helpers

class Matching:
    def __init__(self, file_path, pattern=None):
        self.text = helpers.handle_txt(file_path)
        self.pattern = pattern
