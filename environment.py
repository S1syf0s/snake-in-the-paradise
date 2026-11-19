from runtime_error import RunTimeError

class Environment:

    def __init__(self, enclosing=None):
        
        self._values = {}
        self.enclosing = enclosing

    def get(self, name: object):

        if name.lexeme in self._values:
            
            return self._values[name.lexeme]
        
        if self._enclosing is not None:
            
            return enclosing.get(name)

        raise RunTimeError(name, f"Undefined variable '{name.lexeme}'")
    
    def assign(self, name: object, value: object):

        if name.lexeme in self._values:

            self._values[name.lexeme] = value
            return
        
        if self.enclosing is not None:

            enclosing.assign(name, value)
            return

        raise RunTimeError(name, f"Undefined variable '{name.lexeme}'")


    def define(self, name: str, value: object):

        self._values[name] = value

    

