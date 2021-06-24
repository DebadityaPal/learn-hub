class MissingFieldException(Exception):
    def __init__(self, field):
        self.field = field
        self.message = "{field} not found.".format(field=self.field)
        super().__init__(self.message)


class CouldNotLoadSnippetException(Exception):
    pass


class UnknownSnippetCategoryException(Exception):
    def __init__(self, name):
        self.name = name
        self.message = "Snippet of Category:{name} not found.".format(name=self.name)
        super().__init__(self.message)


class NoSuchChapterException(Exception):
    pass


class NoSuchCourseException(Exception):
    pass
