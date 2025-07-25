class CityValidationException(Exception):
    def __init__(self, message: str, code: int = 11000):
        self.message = message
        self.code = code
        super().__init__(message)

class DateSearchValidationException(Exception):
    def __init__(self, message: str, code: int = 11000):
        self.message = message
        self.code = code
        super().__init__(message)

class MethodValidationException(Exception):
    def __init__(self, message: str, code: int = 11000):
        self.message = message
        self.code = code
        super().__init__(message)