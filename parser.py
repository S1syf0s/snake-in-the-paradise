from expr import Expr, Binary, Unary, Literal, Grouping
from snake_token.py import Token
from token_type import TokenType

class Parser:

    def __init__(self, tokens: list[Token]):

        self._tokens = tokens
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
    
    def _comparison(self):

        expr = self._term()

        while (self._match(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL)):

            operator = self._previous()
            right = self._term()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def _term(self):

        expr = self._factor()

        while (self._match(MINUS, PLUS)):

            operator = self._previous()
            right = self._factor()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def _factor(self):

        expr = self._unary()
        
        while (self._match(SLASH, STAR)):

            operator = self._previous()
            right = self._unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def _unary(self):

        if self._match(BANG, MINUS):
            
            operator = self._previous()
            right = self._unary()
            return Expr.Unary(operator, right)
        
        return self._primary()

    def _primary(self):

        if self._match(FALSE):

            return Expr.Literal(false)
        
        if self._match(TRUE):

            return Expr.Literal(true)

        if self._match(NIL):

            return Expr.Literal(null)

        if self._match(NUMBER, STRING):

            return Expr.Literal(previous().literal)

        if self._match(LEFT_PAREN):

            expr = self._expression()

            self._consume(RIGHT_PAREN, "Expext ')' after expression")

            return Expr.Grouping(expr)

    def _match(types: tuple(TokenType)):

        for token_type in types:

            if self._check(token_type):

                self._advance()
                return True
        
        return False
    
    def _check(self, token_type):

        if self._is_at_end():

            return False

        return peek().type == type

    def _advance(self): 
        
        if not self._is_at_end():

            self._current += 1

        return self._previous()
    
    def _is_at_end(self):

        return peek().type == EOF

    def _peek(self):

        return self._token[current]

    def _previous(self):

        return self._tokens[current - 1]

    

