import abc
import yaml
from api.exceptions import (
    MissingFieldException,
    CouldNotLoadSnippetException,
    UnknownSnippetCategoryException,
)


class Snippet:
    __metaclass__ = abc.ABCMeta
    _requiredFields_ = None

    def __init__(self, category, prompt, **kwargs):
        """
        Base Class for all the types of Snippets. Creates a Base Snippet Object.
        Then changes the class of the object to its specific sub-class.

        Parameters
        ----------
        category: str
            Type of Snippet, this name will be used to assign the object its specific sub-class. (ex. "Text", "MCQ")
        prompt: str
            The input prompt that will be displayed on the console before the user input for this snippet is taken.
        """
        import api.snippets

        name = (category + "snippet").lower()
        if name in api.snippets.types:
            snip = api.snippets.types[name](category, prompt, **kwargs)
        else:
            raise UnknownSnippetCategoryException(name)

        self.__dict__ = snip.__dict__
        self.__class__ = snip.__class__
        self.check_required(self._requiredFields_)

    def check_required(self, fields):
        """
        Checks if there exists atleast some value for the required fields of the specific snippet.

        Parameters
        ----------
        fields: List
            List of fields that will be checked in the object.
        """
        if not fields:
            return True
        elif type(fields) != list:
            fields = [fields]
        for field in fields:
            if not hasattr(self, field):
                return MissingFieldException(field)
        return True

    def print_prompt(self):
        """Prints the prompt of the Snippet."""
        print(self.prompt)

    @abc.abstractmethod
    def get_response(self, data={}):
        """
        Abstract Method. To be implemented in every Sub-Class that inherits from this as a base class.
        Describes the kind of input and the method of getting that input.
        """
        pass

    @abc.abstractmethod
    def test_response(self, data={}):
        """
        Abstract Method. To be implemented in every Sub-Class that inherits from this as a base class.
        Describes the method of testing the user input for correctness.
        """
        pass

    def serve(self, data={}):
        """
        Serves the Snippet by printing the prompt, taking user input and testing it.
        If Input is incorrect, prints the hint (if available).
        """
        self.prompt()
        while True:
            response = self.get_response(data=data)
            result = self.test_response(response, data=data)
            if result:
                break
            elif not result:
                try:
                    print(self.hint)
                except AttributeError:
                    pass
            else:
                continue

    @classmethod
    def load(cls, file):
        """
        Class Method. Reads a `.yaml`` file and initializes all the Snippet objects from that file.

        Parameters
        ----------
        file: file
            Already opened `.yaml` file that contains information about the snippets in the chapter.
        """
        yaml_file = yaml.safe_load(file)
        snippets = []

        for idx, snip in enumerate(yaml_file):
            snip = dict((k.lower(), v) for k, v in snip.items())
            try:
                snippet = cls(**snip)
                snippets.append(snippet)
            except Exception as e:
                raise CouldNotLoadSnippetException(
                    "Could not load Snippet {idx} in {file}: {exception}".format(
                        idx=idx, file=file.name, exception=e
                    )
                )
        return snippets


class NonConsoleSnippet(Snippet):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category, prompt, **kwargs):
        """
        Initializes a Snippet Object that does not require an Interactive Console.

        Parameters
        ----------
        category: str
            Type of Snippet, this name will be used to assign the object its specific sub-class. (ex. "Text", "MCQ")
        prompt: str
            The input prompt that will be displayed on the console before the user input for this snippet is taken.
        """
        self.category = category
        self.prompt = prompt
        self.__dict__.update(kwargs)
