import api.snippet


class Chapter:
    def __init__(self, snippets):
        self.snippets = snippets

    def serve(self, initial_data={}):
        data = initial_data.copy()
        for snippet in self.snippets:
            submission = snippet.serve(data=data)
            if type(submission) == dict:
                data.update(submission)

        return data

    def verify(self):
        for idx, snippet in enumerate(self.snippets):
            if hasattr(snippet, "verify"):
                snippet.verify()
            else:
                print(
                    "Warning: No verification Test detected. (Snippet {idx})".format(
                        idx=idx
                    )
                )

    @classmethod
    def load(cls, file):
        snippets = api.snippet.Snippet.load(file)
        return cls(snippets)
