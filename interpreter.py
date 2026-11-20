from expr import Expr, Binary, Assing, Variable, Conditional, Unary, Literal, Grouping
from snake_token import Token
from token_type import TokenType
from runtime_error import RunTimeError
from stmt import Stmt, Print, If, Expression, Var, Block
from environment import Environment

import __main__

class Interpreter:
    
    def __init__(self):

        self._environment = Environment()

    def interpret(self, statements: list[Stmt]):

        try:
            for statement in statements:
                
                if isinstance(statement, Expression):

                    value = self.evaluate(statement.expression)
                    print(self._stringify(value))

                else:
                    self._execute(statement)

        except RunTimeError as error:
            __main__.Snake.runtime_error(error)

    def evaluate(self, expr: Expr):

        match expr:

            case Literal(value):

                return value
            
            case Conditional(condition, then_branch, else_branch):

                condition = self.evaluate(condition)
                
                if condition == True:
                    
                    return self.evaluate(then_branch)
                
                else:

                    return self.evaluate(else_branch)

            case Grouping(expression):

                return self.evaluate(expression)
            
            case Unary(operator, right):
                
                right = self.evaluate(right)
            
                match operator.token_type:

                    case TokenType.MINUS:
                        
                        self._check_number_operand(operator, right)
                        return -(float(right))
                    
                    case TokenType.BANG:
                         
                        return not self._is_truthy(right)
            
            case Variable(name):

                return self._environment.get(name)

            case Assing(name, value):

                value = self.evaluate(value)
                
                self._environment.assign(name, value)
                return value

            case Binary(left, operator, right):
                
                if operator.token_type == TokenType.COMMA:

                    self.evaluate(left)
                    return self.evaluate(right)

                left = self.evaluate(left)
                right = self.evaluate(right)

                match operator.token_type:
                    
                    case TokenType.GREATER:
                        
                        self._check_number_operands(operator, left, right)
                        return float(left) > float(right)

                    case TokenType.GREATER_EQUAL:
                        
                        self._check_number_operands(operator, left, right)
                        return float(left) >= float(right)
                    
                    case TokenType.LESS:

                        self._check_number_operands(operator, left, right)
                        return float(left) < float(right)

                    case TokenType.LESS_EQUAL:

                        self._check_number_operands(operator, left, right)
                        return float(left) <= float(right)
                    
                    case TokenType.BANG_EQUAL:

                        return not self._is_equal(left, right) 

                    case TokenType.EQUAL_EQUAL:

                        return self._is_equal(left, right)

                    case TokenType.MINUS:

                        self._check_number_operands(operator, left, right)
                        return float(left) - float(right)

                    case TokenType.PLUS:
                        
                        if isinstance(left, float) and isinstance(right, float):
                            
                            return float(left) + float(right)

                        if isinstance(left, str) and isinstance(right, str):

                            return left + right
                        
                        if isinstance(left, str) and isinstance(right, float):

                            string = left + str(right)
                            
                            if string.endswith("0"):

                                return string[:-2]
                            
                            return string

                        if isinstance(left, float) and isinstance(right, str):
                            
                            left_string = str(left)

                            if left_string.endswith("0"):

                                left_string = left_string[:-2]

                            string = left_string + right
                            
                            return string

                        raise RunTimeError(operator, "Operands must be two numbers or two strings")

                    case TokenType.SLASH:

                        self._check_number_operands(operator, left, right)
                        
                        if right == 0:

                            raise RunTimeError(operator, "Division by zero")

                        return float(left) / float(right)

                    case TokenType.STAR:

                        self._check_number_operands(operator, left, right)
                        return float(left) * float(right)
                    
                return None
    
    def _execute(self, stmt: Stmt):

        match stmt:

            case Expression(expression):

                self.evaluate(expression)

            case Print(expression):
                
                value = self.evaluate(expression)
                print(self._stringify(value))

            case Var(name, initializer):
                
                value = None

                if initializer is not None:
                    
                    value = self.evaluate(initializer)
                
                self._environment.define(name.lexeme, value)
                
                return None

            case Block(statements):

                self.execute_block(statements, Environment(self._environment))
                return None
            
            case If(condition, then_branch, else_branch):

                if self._is_truthy(self.evaluate(condition)):
                    
                    self._execute(then_branch)

                elif else_branch is not None:

                    self._execute(else_branch)

                return None

    def execute_block(self, statements, environment):

        previous = self._environment

        try:
            self._environment = environment

            for statement in statements:

                self._execute(statement)
                
        finally:
            self._environment = previous

    def _is_truthy(self, value: object):

        if value is None:

            return False

        if isinstance(value, bool):

            return value

        return True
    
    def _is_equal(self, left: object, right: object):

        if left is None and right is None:

            return True
        
        if left is None:

            return False
        
        return left == right
    
    def _check_number_operand(self, operator: Token, operand: object):

        if isinstance(operand, float):

            return

        raise RunTimeError(operator, "Operand must be a number")

    def _check_number_operands(self, operator: Token, left: object, right: object):

        if isinstance(left, float) and isinstance(right, float):

            return

        raise RunTimeError(operator, "Operands must be numbers")
    
    def _stringify(self, obj: object):

        if obj == None:
            return "nil"
        
        if isinstance(obj, bool):

            return str(obj).lower()

        if isinstance(obj, float):
            
            text = str(obj)
            
            if text.endswith("0"):
                text = text[:-2]
            
            return text 

        return str(obj)


