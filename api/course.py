import os
from api.exceptions import NoSuchChapterException, NoSuchCourseException
import unicodedata
import re
import yaml
import api.chapter


class Course:
    def __init__(self, author, course, chapters, path, description=None):
        self.author = author
        self.course = course
        self.chapters = chapters.split(";")
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
            print("{idx} - {chapter}".format(idx=idx + 1, chapter=chapter))

    def verify(self):
        for field in ["course", "chapters", "author", "description", "organization"]:
            if not hasattr(self, field):
                print("course.yaml has no '{field}' attribute".format(field=field))

        for idx in range(1, len(self.chapters) + 1):
            chapter = self.load_chapter(idx)
            if hasattr(chapter, "verify"):
                chapter.verify()
            else:
                print(
                    "Warning: No verification test detected. (Chapter {id}".format(
                        id=idx + 1
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
        chapter.serve(
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

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, "course.yaml"), "r") as f:
            yaml_file = yaml.safe_load(f)
            if len(yaml_file) < 1:
                raise NoSuchCourseException()
            kwargs_dict = dict((k.lower(), v) for k, v in yaml_file[0].items())
            course = cls(path=path, **kwargs_dict)
        return course
