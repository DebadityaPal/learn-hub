import abc
import yaml
from api.console import Console, Recorder
from api.exceptions import (
    MissingFieldException,
    CouldNotLoadSnippetException,
    UnknownSnippetCategoryException,
)
from api.colors import print_prompt, print_hints


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
        print_prompt(self.prompt)

    @abc.abstractmethod
    def get_response(self, data={}):
        """
        Abstract Method. To be implemented in every Sub-Class that inherits from this as a base class.
        Describes the kind of input and the method of getting that input.
        """
        pass

    @abc.abstractmethod
    def test_response(self, response, data={}):
        """
        Abstract Method. To be implemented in every Sub-Class that inherits from this as a base class.
        Describes the method of testing the user input for correctness.
        """
        pass

    def serve(self, data={}):
        """
        Serves the Snippet by printing the prompt, taking user input and testing it.
        """
        self.print_prompt()
        while True:
            response = self.get_response(data=data)
            result = self.test_response(response, data=data)
            if result:
                break
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


class ConsoleSnippet(Snippet):
    __metaclass__ = abc.ABCMeta
    _requiredFields_ = []

    def __init__(self, category, prompt, **kwargs):
        """
        Initializes a Snippet Object that requires an Interactive Console.

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
        if hasattr(self, "yaml_hook"):
            self.yaml_hook()

    def new_console(self, local_variables):
        """
        Initializes a new console with a set of local variables.

        Parameters
        ----------
        local_variables: dict
            The dictionary of local varaibles with their values to be created.
        """
        self._recorder = Recorder()
        new_locals = local_variables.copy()
        new_locals["__ast_parser__"] = self._recorder
        return Console(new_locals)

    def serve(self, data={}):
        """
        Serves the Snippet by printing the prompt, taking user input and testing it.
        """
        self.print_prompt()
        while True:
            if "state" not in data:
                data["state"] = dict()
            # Manual DeepCopy
            deepcopy_state = {}
            for key, value in data["state"].items():
                deepcopy_state[key] = value
            for value in self.get_response(data=deepcopy_state):
                if self.test_response(value, data=deepcopy_state):
                    data["state"].update(value["added"])
                    data["state"].update(value["changed"])
                    for var in value["removed"]:
                        del data["state"][var]
                    return data
                else:
                    try:
                        print_hints(self.hints)
                    except AttributeError:
                        pass
                    break
