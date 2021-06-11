import abc
from api.exceptions import MissingFieldException


class Snippet:
    __metaclass__ = abc.ABCMeta
    _requiredFields_ = None

    def __init__(self, category, prompt, **kwargs):
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

    def prompt(self):
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
