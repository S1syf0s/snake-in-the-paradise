from expr import Expr, Binary, Unary, Literal, Grouping
from snake_token.py import Token
from token_type import TokenType

class Parser:

    def __init__(self, tokens: list[Token]):

        self._tokens = []
        self._current = 0
    
    def _expression(self):

        return self._equality()

    def _equality(self):

        expr = self._comparison()
        
        while (match(BANG_EQUAL, EQUAL_EQUAL)):

            operator = self._previous()
            right = self._comparison()
            
            expr = Expr.Binary(expr, operator, right)

        return expr 
    
    def _match(types: list[Token]):

        for token_type in types:

            if (check(token_type)):
                advance()
                return True
        
        return False
    
    def _check(self, token_type):

        if (self._is_at_end()):

            return False

        return peek().type == type

    def _advance(self): 
        
        if (not self._is_at_end()):

            self._current += 1

        return self._previous()
    
    def _is_at_end(self):

        return peek().type == EOF

    def _peek(self):

        return self._token[current]

    def _previous(self):

        return self._tokens[current - 1]







