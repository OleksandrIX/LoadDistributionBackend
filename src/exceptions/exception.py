class UnauthorizedException(Exception):
    def __init__(self, massage=None):
        self.status_code = 401
        self.massage = massage or "Unauthorized"


class ForbiddenException(Exception):
    def __init__(self, massage=None):
        self.status_code = 403
        self.massage = massage or "Forbidden"
