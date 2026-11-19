from runtime_error import RunTimeError

class Environment:

    def __init__(self):

        self._values = {}

    def get(self, name: object):

        if name.lexeme in self._values:
            
            return self._values[name.lexeme]

        raise RunTimeError(name, f"Undefined variable '{name.lexeme}'")
    
    def define(self, name: str, value: object):

        self._values[name] = value

    

