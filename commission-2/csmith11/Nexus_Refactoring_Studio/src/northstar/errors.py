class NorthstarError(Exception):
    """Base exception for platform errors."""

class ValidationError(NorthstarError):
    pass

class CustomerNotFoundError(NorthstarError):
    pass
