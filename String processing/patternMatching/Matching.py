from patternMatching import helpers


class Matching:
    def __init__(self, file_path, pattern=None):
        self.__pattern_length, self.__text_length = None, None

        self.text = helpers.handle_txt(file_path)
        self.pattern = pattern

    @property
    def pattern(self):
        return self.__pattern

    @pattern.setter
    def pattern(self, pattern):
        self.__pattern = pattern
        self.__pattern_length = len(self.__pattern)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
        self.__text_length = len(self.__text)

    @property
    def text_length(self):
        return self.__text_length

    @property
    def n(self):
        return self.__text_length

    @property
    def m(self):
        return self.__pattern_length