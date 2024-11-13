class InvalidUserException(Exception):
    def __init__(self,  detail, message):
        self.status = 400
        self.detail = detail
        self.message = message

class InvalidDataException(Exception):
    def __init__(self, detail, message):
        self.status = 422
        self.detail = detail
        self.message = message

class UserNotFound(Exception):
    def __init__(self, username):
        self.status = 404
        self.username = username