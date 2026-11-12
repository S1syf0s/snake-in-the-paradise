from token_type import TokenType
from snake_token import Token

import __main__

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
    
    def _string(self):

        while self._peek() != '"' and not self._is_at_end():

            if self._peek() == '\n':
                self._line += 1

            self._advance()

        if self._is_at_end():
            __main__.Snake.error(self._line, "You took a bite, but please close the string")
            return 

        self._advance()
        
        value = self._source[self._start + 1:self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _scan_token(self):
        
        c = self._advance()
        
        match c:

            case '(':
                self._add_token(TokenType.LEFT_PAREN)
            
            case ')':
                self._add_token(TokenType.RIGHT_PAREN)
            
            case '{':
                self._add_token(TokenType.LEFT_BRACE)

            case '}':
                self._add_token(TokenType.RIGHT_BRACE)

            case ',':
                self._add_token(TokenType.COMMA)

            case '.':
                self._add_token(TokenType.DOT)

            case '-':
                self._add_token(TokenType.MINUS)

            case '+':
                self._add_token(TokenType.PLUS)

            case ';':
                self._add_token(TokenType.SEMICOLON)
            
            case '*':
                self._add_token(TokenType.STAR)
            
            case '!':
                self._add_token(BANG_EQUAL if self._match('=') else BANG)

            case '=':
                self._add_token(EQUAL_EQUAL if self._match('=') else EQUAL)

            case '<':
                self._add_token(LESS_EQUAL if self._match('=') else LESS)

            case '>':
                self._add_token(GREATER_EQUAL if self._match('=') else GREATER)

            case '/':
                
                if self._match('/'):
                    while self._peek() != '\n' and not self._is_at_end():
                        self._advance()
                
                else:
                    self._add_token(TokenType.SLASH)
            
            case ' ':
                pass

            case '\r':
                pass

            case '\t':
                pass

            case '\n':
                self._line += 1

            case '"':
                self._string()

            case _:
                __main__.Snake.error(self._line, "God is angry and Eve is hungry")

    def _is_at_end(self):
        
        return self._current >= len(self._source) 
    
    def _advance(self):
        
        char = self._source[self._current]
        self._current += 1
        return char
    
    def _add_token(self, token_type: TokenType, literal=None):
        
        text = self._source[self._start:self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))   
    
    def _match(self, expected: str):

        if self._is_at_end():
            return False

        if (self._source[self._current] != expected):
            return False
        
        self._current += 1
        return True
    
    def _peek(self):

        if self._is_at_end():
            return '\0'
        
        return self._source[self._current]



