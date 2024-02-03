class FastApiAuthException(Exception):
    ...


class UserAlreadyExists(FastApiAuthException):
    ...


class ValidationError(FastApiAuthException):
    ...
