class ClientException(Exception):
    def __init__(self, status_code: int = 400, message: str = "Bad request"):
        self.status_code = status_code
        self.message = message


class UnauthorizedException(Exception):
    def __init__(self, message=None):
        self.status_code = 401
        self.message = message or "Unauthorized"


class ForbiddenException(Exception):
    def __init__(self, message=None):
        self.status_code = 403
        self.message = message or "Forbidden"
