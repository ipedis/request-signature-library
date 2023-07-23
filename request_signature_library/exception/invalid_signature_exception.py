class InvalidSignatureException(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = 'Request does not match.'
        super().__init__(message)
