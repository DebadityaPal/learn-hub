from api.snippet import NonConsoleSnippet


class TextSnippet(NonConsoleSnippet):

    _requiredFields_ = []

    def execute(self, data={}):
        self.print_prompt()
        self.get_response()

    def get_response(self, data={}):
        response = input("...")
