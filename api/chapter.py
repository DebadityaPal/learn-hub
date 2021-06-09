class Chapter:
    def __init__(self, snippets):
        self.snippets = snippets

    def execute(self):
        data = {}
        for snippet in self.snippets:
            # TODO: Create Class for snippets
            submission = snippet.execute(data=data)
            if type(submission) == dict:
                data.update(submission)

        return data

    def verify(self):
        # for idx, snippet in enumerate(self.snippets):
        # TODO: Test for snippets

    @classmethod
    def load(cls, path):
        # TODO: Load yaml file
        return
