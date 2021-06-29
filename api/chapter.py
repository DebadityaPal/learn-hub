import api.snippet


class Chapter:
    def __init__(self, snippets):
        """
        Creates a Chapter object containing all the relevant snippets.

        Parameters
        ----------
        snippets: List
            List of Snippets contained  in the `chapter.yaml` file.
        """
        self.snippets = snippets

    def serve(self, initial_data={}):
        """Iterates over each snippet and serves it on the console."""
        data = initial_data.copy()
        for snippet in self.snippets:
            submission = snippet.serve(data=data)
            if type(submission) == dict:
                data.update(submission)

        return data

    def verify(self):
        """Verifies the Snippet if it has a test available."""
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
        """
        Class Method. Loads a Chapter from an already opened file. 
        Also forwards the file to initialize all the Snippets.

        Parameters
        ----------
        file: file
            Already opened `.yaml` file that contains details of Snippets in the chapter.
        """
        snippets = api.snippet.Snippet.load(file)
        return cls(snippets)
