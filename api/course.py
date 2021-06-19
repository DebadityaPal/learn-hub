import os
from api.exceptions import NoSuchChapterException
import unicodedata
import re
import api.chapter


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

    def verify(self):
        for field in [
            "course",
            "chapters",
            "author",
            "description",
            "organization",
            "version",
        ]:
            if not hasattr(self, field):
                print("course.yaml has no '{field}' attribute".format(field=field))

        for idx, chapter in enumerate(self.chapters):
            if hasattr(chapter, "verify"):
                chapter.verify()
            else:
                print(
                    "Warning: No verification test detected. (Chapter {idx}".format(
                        idx=idx
                    )
                )

    def serve(self):
        while True:
            self.contents()
            try:
                print("Selection:")
                chapter_id = input().strip()
                self.serve_chapter(chapter_id)
            except NoSuchChapterException:
                print("No Chapter found at index: {idx}".format(idx=chapter_id))
            except EOFError:
                print("Error: EOF Reached")
                break

    def serve_chapter(self, chapter_id):
        chapter = self.load_chapter(chapter_id)
        data = chapter.execute(
            initial_data={
                "path": self.path,
            }
        )
        print("End Of Chapter! See you soon.")

    def load_chapter(self, chapter_id):
        name = ""
        try:
            chapter_id = int(chapter_id)
        except ValueError:
            pass

        if type(chapter_id) == int:
            try:
                name = self.chapters[chapter_id - 1]
            except IndexError:
                raise NoSuchChapterException("Invalid Lesson Index")
        else:
            try:
                name = self.chapters[self.chapters.index(chapter_id)]
            except ValueError:
                raise NoSuchChapterException("Invalid lesson {name}".format(name=name))

        chapter_path = os.path.join(self.path, "chapters", self.slugify(name) + ".yaml")

        with open(chapter_path, "r") as f:
            chapter = api.chapter.Chapter.load(f)

        return chapter

    def slugify(self, text):
        text = str(text)
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        text = re.sub(r"[^\w\s-]", "", text.lower())
        return re.sub(r"[-\s]+", "-", text).strip("-_")
