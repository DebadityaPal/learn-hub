class MissingFieldException(Exception):
    def __init__(self, field):
        self.field = field
        self.message = "{field} not found.".format(field=field)
        super().__init__(self.message)
