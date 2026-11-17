from snake_token import Token

class RunTimeError(Exception):

    def __init__(self, token: Token, message: str):

        super().__init__(message)
        self.token = token
