from expr import Expr, Binary, Conditional, Unary, Literal, Grouping
from snake_token import Token
from token_type import TokenType

import __main__

class ParseError(Exception):
    pass

class Parser:

    def __init__(self, tokens: list[Token]):

        self._tokens = tokens
        self._current = 0

    def parse(self):

        try:
            return self._expression()
        
        except ParseError as error:
            return None

    def _expression(self):

        expr = self._conditional()

        while (self._match(TokenType.COMMA)):

            operator = self._previous()
            right = self._conditional()

            expr = Binary(expr, operator, right)
         
        return expr

    def _conditional(self):
        
        expr = self._equality()

        if self._match(TokenType.QUESTION):
            
            condition = expr
            
            then_branch = self._equality()

            if self._consume(TokenType.COLON, "expected ':' after branch"):

                else_branch = self._conditional()

            expr = Conditional(condition, then_branch, else_branch)

        return expr

    def _equality(self):

        expr = self._comparison()
        
        while (self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):

            operator = self._previous()
            right = self._comparison()
            
            expr = Binary(expr, operator, right)

        return expr 

    def _comparison(self):

        expr = self._term()

        while (self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):

            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)

        return expr
    
    def _term(self):

        expr = self._factor()

        while (self._match(TokenType.MINUS, TokenType.PLUS)):

            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def _factor(self):

        expr = self._unary()
        
        while (self._match(TokenType.SLASH, TokenType.STAR)):

            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self):

        if self._match(TokenType.BANG, TokenType.MINUS):
            
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        
        return self._primary()

    def _primary(self):

        if self._match(TokenType.FALSE):

            return Literal(False)
        
        if self._match(TokenType.TRUE):

            return Literal(True)

        if self._match(TokenType.NIL):

            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):

            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):

            expr = self._expression()

            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")

            return Grouping(expr)
        
        raise self._error(self._peek(), "Expect expression")

    def _match(self, *types: TokenType):

        for token_type in types:

            if self._check(token_type):

                self._advance()
                return True
        
        return False

    def _consume(self, token_type: TokenType, message: str):

        if self._check(token_type):

            return self._advance()
        
        raise self._error(self._peek(), message)

    def _check(self, token_type):

        if self._is_at_end():

            return False

        return self._peek().token_type == token_type

    def _advance(self): 
        
        if not self._is_at_end():

            self._current += 1

        return self._previous()
    
    def _is_at_end(self):

        return self._peek().token_type == TokenType.EOF

    def _peek(self):

        return self._tokens[self._current]

    def _previous(self):

        return self._tokens[self._current - 1]
    
    def _error(self, token: Token, message: str):
        
        __main__.Snake.error(token, message)
        return ParseError() 
    
    def _synchronize(self):

        self._advance()

        while not self._is_at_end():

            if self._previous().token_type == TokenType.SEMICOLON:
                return

            match self._peek().token_type:

                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return

            self._advance()


