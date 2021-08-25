import ast
from api.snippet import ConsoleSnippet
from api.colors import print_error


class codeSnippet(ConsoleSnippet):
    _requiredFields_ = ["answer"]

    def get_response(self, data={}):
        """Initializes a console and fetches user code input."""
        console = self.new_console(data)
        for value in console.interact(""):
            yield value

    def test_response(self, response, data={}):
        """Checks user code input for correctness by matching ASTs with author's answer."""
        return ast.dump(self.answer_tree) == ast.dump(response["ast"])

    def yaml_hook(self):
        """Parses author's answer into an AST ready for comparison."""
        self.answer_tree = ast.parse(self.answer, filename="<answer>", mode="single")

    def verify(self):
        """Checks if prompt is a string variable or not."""
        if type(self.prompt) != str:
            print_error(
                "Prompt is of type: {type}, expected str.".format(
                    type=type(self.prompt)
                )
            )
