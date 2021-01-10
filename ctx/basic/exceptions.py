class CtxException(Exception):
    """An exception that Ctx can handle and show to the user."""
    def __init__(self, message: str):
        super(CtxException, self).__init__(self, message)
        self.message = message

    def __str__(self, *args, **kwargs):  # real signature unknown
        """ Return str(self). """
        return self.message
