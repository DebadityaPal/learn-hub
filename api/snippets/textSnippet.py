from api.snippet import NonConsoleSnippet


class textSnippet(NonConsoleSnippet):

    _requiredFields_ = []

    def get_response(self, data={}):
        """Takes in a key press as user input."""
        input("...")

    def test_response(self, response, data={}):
        print("\n")
        return True

    def verify(self):
        """Verifies if Snippet prompt is a string."""
        if type(self.prompt) != str:
            print(
                "Prompt is of type: {type}, expected str.".format(
                    type=type(self.prompt)
                )
            )
