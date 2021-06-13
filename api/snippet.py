import abc
import yaml
from api.exceptions import MissingFieldException, CouldNotLoadSnippetException


class Snippet:
    __metaclass__ = abc.ABCMeta
    _requiredFields_ = None

    def __init__(self, category, prompt, **kwargs):
        import api.snippets
        # TODO: Create Subclass Object

        self.verify(self._requiredFields_)

    def verify(self, fields):
        if not fields:
            return True
        elif type(fields) != list:
            fields = [fields]
        for field in fields:
            if not hasattr(self, field):
                return MissingFieldException(field)
        return True

    def print_prompt(self):
        print(self.prompt)

    @abc.abstractmethod
    def get_response(self, data={}):
        pass

    @abc.abstractmethod
    def test_response(self, data={}):
        pass

    def execute(self, data={}):
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
        yaml_file = yaml.safe_load(file)
        snippets = []

        for idx, snip in enumerate(yaml_file):
            snip = dict((k.lower(), v) for k, v in snip.items())
            try:
                snippet = cls(**snip)
                snippets.append(snippet)
            except Exception as e:
                raise CouldNotLoadSnippetException(
                    "Could not load Question {idx} in {file}: {exception}".format(
                        idx=idx, file=file.name, exception=e
                    )
                )
        return snippets


class NonConsoleSnippet(Snippet):
    __metaclass__ = abc.ABCMeta

    def __init__(self, category, prompt, **kwargs):
        self.category = category
        self.prompt = prompt
        self.__dict__.update(kwargs)
