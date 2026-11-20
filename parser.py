from expr import *
from snake_token import Token
from token_type import TokenType
from stmt import *

import __main__

class ParseError(Exception):
    pass

class Parser:

    def __init__(self, tokens: list[Token]):

        self._tokens = tokens
        self._current = 0

    def parse(self):
        
        statements = []

        while not self._is_at_end():
            
            statements.append(self._declaration())

        return statements

    def _expression(self):

        expr = self._assignment()

        while (self._match(TokenType.COMMA)):

            operator = self._previous()
            right = self._assignment()

            expr = Binary(expr, operator, right)
         
        return expr
    
    def _declaration(self):
        
        try:
            if self._match(TokenType.VAR):

                return self._var_declaration()
            
            return self._statement()
        
        except ParseError as error:
            
            self._synchronize()
            return None

    def _statement(self):

        if self._match(TokenType.FOR):

            return self._for_statement()

        if self._match(TokenType.IF):

            return self._if_statement()

        if self._match(TokenType.PRINT):
        
            return self._print_statement()

        if self._match(TokenType.WHILE):

            return self._while_statement()

        if self._match(TokenType.LEFT_BRACE):

            return Block(self._block())

        return self._expression_statement()

    def _for_statement(self):

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'")

        initializer = None

        if self._match(TokenType.SEMICOLON):

            initializer = None
        
        elif self._match(TokenType.VAR):

            initializer = self._var_declaration()

        else:

            initializer = self._expression_statement()
        
        condition = None

        if not self._check(TokenType.SEMICOLON):

            condition = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition")

        increment = None

        if not self._check(TokenType.RIGHT_PAREN):

            increment = self._expression()

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses")
        
        body = self._statement()
    
        if increment is not None:
            
            body = Block([body, Expression(increment)])
        
        if condition is None:

            condition = Literal(True)

        body = While(condition, body)

        if initializer is not None:

            body = Block([initializer, body])

        return body

    def _if_statement(self):

        self._consume(TokenType.LEFT_PAREN, "Expect '(' after if")

        condition = self._expression()

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if")

        then_branch = self._statement()
        else_branch = None

        if self._match(TokenType.ELSE):

            else_branch = self._statement()
        
        return If(condition, then_branch, else_branch)

    def _print_statement(self):
        
        value = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after value")

        return Print(value)

    def _var_declaration(self):
        
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name")
        
        initializer = None

        if self._match(TokenType.EQUAL):

            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return Var(name, initializer)
    
    def _while_statement(self):

        self._consume(TokenType.LEFT_PAREN, "Expect '(' afrer 'while'")

        condition = self._expression()

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition")

        body = self._statement()

        return While(condition, body)

    def _expression_statement(self):

        expr = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after expression")

        return Expression(expr)

    def _block(self):

        statements = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():

            statements.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block")
        return statements

    def _assignment(self):

        expr = self._conditional()
        
        if self._match(TokenType.EQUAL):

            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, Variable):

                name = expr.name
                return Assing(name, value)
            
            self._error(equals, "Invalid assignment target")

        return expr

    def _conditional(self):
        
        expr = self._or()

        if self._match(TokenType.QUESTION):
            
            condition = expr
            
            then_branch = self._expression()

            if self._consume(TokenType.COLON, "expected ':' after branch"):

                else_branch = self._conditional()

            expr = Conditional(condition, then_branch, else_branch)

        return expr
    
    def _or(self):

        expr = self._and()

        while self._match(TokenType.OR):

            operator = self._previous()
            right = self._and()
            expr = Logical(expr, operator, right)

        return expr

    def _and(self):

        expr = self._equality()

        while self._match(TokenType.AND):

            operator = self._previous()
            right = self._equality()
            expr = Logical(expr, operator, right)

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

        if self._match(TokenType.IDENTIFIER):

            return Variable(self._previous())

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

