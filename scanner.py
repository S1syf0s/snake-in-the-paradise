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
        self._keywords = {}
    
        self._keywords["and"] = TokenType.AND
        self._keywords["class"] = TokenType.CLASS
        self._keywords["else"] = TokenType.ELSE
        self._keywords["false"] = TokenType.FALSE
        self._keywords["for"] = TokenType.FOR
        self._keywords["fun"] = TokenType.FUN
        self._keywords["if"] = TokenType.IF
        self._keywords["nil"] = TokenType.NIL
        self._keywords["or"] = TokenType.OR
        self._keywords["print"] = TokenType.PRINT
        self._keywords["return"] = TokenType.RETURN
        self._keywords["super"] = TokenType.SUPER
        self._keywords["this"] = TokenType.THIS
        self._keywords["true"] = TokenType.TRUE
        self._keywords["var"] = TokenType.VAR
        self._keywords["while"] = TokenType.WHILE

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
                self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)

            case '=':
                self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)

            case '<':
                self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)

            case '>':
                self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)

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
                
                if self._is_digit(c):
                    self._number()
                
                elif self._is_alpha(c):
                    self._identifier()

                else:
                    __main__.Snake.error(self._line, "God is angry and Eve is hungry")
    
    def _identifier(self):
        
        while self._is_alpha_numeric(self._peek()):
            self._advance()
        
        text = self._source[self._start:self._current]
        
        if text in self._keywords:
            self._add_token(self._keywords[text])
            return

        self._add_token(TokenType.IDENTIFIER)
            
    def _number(self):
        
        while self._is_digit(self._peek()):
            self._advance()
        
        if self._peek() == '.' and self._is_digit(self._peek_next()):
            self._advance()
            
            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER, self._source[self._start:self._current]) 

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
    
    def _peek_next(self):
        
        if self._current + 1 >= len(self._source): 
            return '\0'
    
        return self._source[self._current + 1]
    
    def _is_alpha_numeric(self, c: str):

        return self._is_alpha(c) or self._is_digit(c)

    def _is_alpha(self, c:str):

        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'
   
    def _is_digit(self, c: str):
        
        return c >= '0' and c <= '9'

