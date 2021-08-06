import os
from api.exceptions import NoSuchChapterException, NoSuchCourseException
import unicodedata
import re
import sys
import yaml
import api.chapter


class Course:
    def __init__(self, author, course, chapters, path, **kwargs):
        """Creates a new Course object, that parses details from a `course.yaml` file.

        Parameters
        ----------
        author: str
            The name of the author(s) who created the course.
        course: str
            The name of the course, it should ideally be descriptive. (ex. "Hub Datasets")
        chapters: str
            The names of the chapters separated by semi-colons (;), the delimiter is important.
        path: str
            The directory path where the course.yaml file is located.
        description: str, optional
            A  short and precise description of the course.
        organization: str, optional
            The organization the author belongs to. Could be `None` if no affiliation is to be shown.
        """
        self.author = author
        self.course = course
        self.chapters = chapters
        self.path = path
        self.description = None
        self.__dict__.update(kwargs)
        self.verify()

    def describe(self):
        """
        Prints the
        - Name of the Course
        - Name of the Author(s)
        - Description of the Course (if available)
        """
        if self.description:
            print(
                "{course} by {author}: {description}".format(
                    course=self.course, author=self.author, description=self.description
                )
            )
        else:
            print("{course} by {author}".format(course=self.course, author=self.author))

    def contents(self):
        """Lists the chapters in the course in an indexed manner."""
        print("Table of Contents:")
        for idx, chapter in enumerate(self.chapters):
            print("{idx} - {chapter}".format(idx=idx + 1, chapter=chapter))

    def verify(self):
        """
        Checks if the Course has atleast some value for the essential fields.
        Then checks if each Chapter has a verification test,
        if yes, then the test is carried out.
        """
        for field in ["course", "chapters", "author"]:
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
        """Gives the user the contents of the course and asks the user to select a chapteṛ."""
        while True:
            self.contents()
            try:
                print("{idx} - Exit".format(idx=len(self.chapters) + 1))
                print("Selection: ", end="")
                chapter_id = input().strip()
                if chapter_id == str(len(self.chapters) + 1):
                    sys.exit(0)
                self.serve_chapter(chapter_id)
            except NoSuchChapterException:
                print("No Chapter found at index: {idx}".format(idx=chapter_id))
            except EOFError:
                print("Error: EOF Reached")
                break

    def serve_chapter(self, chapter_id):
        """
        Takes the user's chapter selection and loads the chapter into memory. Then proceeds to serve the chapter.

        Parameters
        ----------
        chapter_id: int
            The index of the chapter selected by the user (Indexes starting from 1).
        """
        chapter = self.load_chapter(chapter_id)
        initial_data = {
            "path": self.path,
        }
        chapter.serve(initial_data)
        print("End Of Chapter! See you soon.")

    def load_chapter(self, chapter_id):
        """
        Takes the user's chapter selection and verifies if it is a proper selection.
        Then loads the `chapter.yaml` file into memory and return the Chapter object.

        Parameters
        ----------
        chapter_id: int
            The index of the chapter selected by the user (Indexes starting from 1).
        """
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
        """
        Converts normal text to file name approved slugs, by removing forbidden characters and
        replacing spaces with "-".

        Parameters
        ----------
        text: str
            The normal text that needs to be converted into a slug.
        """
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
        """
        A class method responsible for loading the Course from the `course.yaml`
        file into an object of the Class.

        Parameters
        ----------
        path: str
            The directory path where the `course.yaml` file can be found.
        """
        with open(os.path.join(path, "course.yaml"), "r") as f:
            yaml_file = yaml.safe_load(f)
            if len(yaml_file) < 1:
                raise NoSuchCourseException()
            kwargs_dict = dict((k.lower(), v) for k, v in yaml_file[0].items())
            course = cls(path=path, **kwargs_dict)
        return course
