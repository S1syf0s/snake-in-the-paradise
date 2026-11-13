from expr import Expr, Binary, Unary, Literal, Grouping
from snake_token import Token
from token_type import TokenType

class AstPrinter:

    def print_expr(self, expr: Expr):
        
        match expr:

            case Literal(value):

                if value is None:
                    return "nil"

                return str(value)

            case Grouping(expression):
                
                return self._parenthesize("group", expression)
            
            case Unary(operator, right):

                return self._parenthesize(operator.lexeme, right)

            case Binary(left, operator, right):

                return self._parenthesize(operator.lexeme, left, right)
        
    def _parenthesize(self, name: str, *exprs: Expr):

        result = "(" + name

        for expr in exprs:
            result += " " + self.print_expr(expr)
            
        result += ")"
        return result

    @staticmethod
    def main(args: list[str]):

        expression = Binary(
                Unary(
                    Token(TokenType.MINUS, "-", None, 1),
                    Literal(123)
                    ),
                Token(TokenType.STAR, "*", None, 1),
                Grouping(Literal(45.67))
                )

        print(AstPrinter().print_expr(expression))

if __name__=="__main__":
    AstPrinter.main([])





