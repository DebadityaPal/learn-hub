from api.snippet import NonConsoleSnippet
from api.colors import print_error


class textSnippet(NonConsoleSnippet):

    _requiredFields_ = []

    def get_response(self, data={}):
        """Takes in a key press as user input."""
        input("...")

    def test_response(self, response, data={}):
        return True

    def verify(self):
        """Verifies if Snippet prompt is a string."""
        if type(self.prompt) != str:
            print_error(
                "Prompt is of type: {type}, expected str.".format(
                    type=type(self.prompt)
                )
            )
