from token_type import TokenType
from token import Token

class Scanner:
    
    def __init__(self, source: str):
        
        self._source = source
        self._tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
    
    def scan_tokens(self):
        
        while not self._is_at_end():
            
            self._start = self._current
            self._scan_token() 

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens
    
    def _scan_token(self):
        
        c = self.advance()
        
        match c:

            case '(':
                self._add_token(TokenType.LEFT_PAREN)
                break
            
            case ')':
                self._add_token(TokenType.RIGH_PAREN)
                break

    def _is_at_end(self):
        
        return self._current >= len(self._source) 
    
    def _advance(self):
        
        char = self._source[self._current]
        self._current += 1
        return char
    
    def _add_token(self, token_type: TokenType, literal=None):
        
        text = 
    
    





   





