from snake_token.py import Token

class Parser:

    def __init__(self, tokens: list[Token]):

        self._tokens = []
        self._current = 0
    
    def expression(self):

        return equality()

    def equality(self):

        while (mathch
