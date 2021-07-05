from api.snippet import NonConsoleSnippet
import random


class mcqSnippet(NonConsoleSnippet):

    _requiredFields_ = ["options", "answer"]

    def get_response(self, data={}):
        options = self.options
        random.shuffle(options)

        while True:
            for index, option in enumerate(options):
                print("{idx}. {option}".format(idx=index + 1, option=option))
            try:
                answer = int(input("Select your answer: ")) - 1
                return options[answer]
            except (ValueError, IndexError):
                print(
                    "Invalid Option. Make sure your choice is between 1 and {num_op}".format(
                        num_op=len(options)
                    )
                )
                continue

    def test_response(self, response, data={}):
        return response == self.answer

    def verify(self):
        if self.answer not in self.options:
            print("Choices must contain answer.")
