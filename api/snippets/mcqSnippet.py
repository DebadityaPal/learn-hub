from api.snippet import NonConsoleSnippet
from api.exceptions import OptionHintMismatchException
from api.colors import print_error, print_hints, print_prompt, print_option
import random


class mcqSnippet(NonConsoleSnippet):

    _requiredFields_ = ["options", "answer"]

    def get_response(self, data={}):
        """Fetches an option from the user and checks if it is a valud option."""
        self.option_indexes = list(range(len(self.options)))
        random.shuffle(self.option_indexes)
        while True:
            for idx, option_idx in enumerate(self.option_indexes):
                print_option(
                    "{idx}. {option}".format(
                        idx=idx + 1, option=self.options[option_idx]
                    )
                )
            try:
                answer = int(input("Select your answer: ")) - 1
                return self.option_indexes[answer]
            except (ValueError, IndexError):
                print_error(
                    "Invalid Option. Make sure your choice is between 1 and {num_op}".format(
                        num_op=len(self.options)
                    )
                )
                continue

    def test_response(self, response, data={}):
        """Tests if the user's answer is the correct answer."""
        if type(self.hints) == str:
            if self.options[response] != self.answer:
                print_hints(self.hints)
        elif type(self.hints) == list:
            try:
                print_hints(self.hints[response])
            except IndexError:
                if len(self.hints) > 0:
                    print_hints(self.hints[0])
                else:
                    pass
        return self.options[response] == self.answer

    def verify(self):
        """Checks if the correct answer is present as an option."""
        if self.answer not in self.options:
            print_error("Choices must contain answer.")
        if type(self.hints) == list and len(self.hints) != len(self.options):
            raise OptionHintMismatchException(
                "Expected number of options and hints to match. There are {len_options} options and {len_hints} hints".format(
                    len_options=len(self.options), len_hints=len(self.hints)
                )
            )
