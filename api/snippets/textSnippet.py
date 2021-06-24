from api.snippet import NonConsoleSnippet


class textSnippet(NonConsoleSnippet):

    _requiredFields_ = []

    def serve(self, data={}):
        self.print_prompt()
        self.get_response()

    def get_response(self, data={}):
        input("...")

    def verify(self):
        if type(self.output) != str:
            print(
                "Output is of type: {type}, expected str.".format(
                    type=type(self.output)
                )
            )
