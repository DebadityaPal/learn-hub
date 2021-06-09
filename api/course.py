class Course:
    def __init__(self, author, course, chapters, path, description=None):
        self.author = author
        self.course = course
        self.chapters = chapters
        self.path = path
        self.description = description

    def describe(self):
        if self.description:
            print(
                "{course} by {author}: {description}".format(
                    course=self.course, author=self.author, description=self.description
                )
            )
        else:
            print("{course} by {author}".format(course=self.course, author=self.author))

    def contents(self):
        for idx, chapter in enumerate(self.chapters):
            print("{idx} - {chapter}".format(idx=idx, chapter=chapter))
