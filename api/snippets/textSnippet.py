from api.snippet import NonConsoleSnippet


class textSnippet(NonConsoleSnippet):

    _requiredFields_ = []

    def serve(self, data={}):
        """Serves the snippet in the console. Prints input prompt and waits for user to provide input."""
        self.print_prompt()
        self.get_response()

    def get_response(self, data={}):
        """Takes in a key press as user input."""
        input("...")

    def verify(self):
        """Verifies if Snippet prompt is a string."""
        if type(self.prompt) != str:
            print(
                "Prompt is of type: {type}, expected str.".format(
                    type=type(self.prompt)
                )
            )
