import ast
from api.snippet import ConsoleSnippet
from api.colors import print_error


class codeSnippet(ConsoleSnippet):
    _requiredFields_ = ["answer"]

    def get_response(self, data={}):
        console = self.new_console(data)
        for value in console.interact(""):
            yield value

    def test_response(self, response, data={}):
        return ast.dump(self.answer_tree) == ast.dump(response["ast"])

    def yaml_hook(self):
        self.answer_tree = ast.parse(self.answer, filename="<answer>", mode="single")

    def verify(self):
        if type(self.prompt) != str:
            print_error(
                "Prompt is of type: {type}, expected str.".format(
                    type=type(self.prompt)
                )
            )
