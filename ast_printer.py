from expr import Expr, Binary, Unary, Literal, Grouping
from token import Token
from token_type import TokenType

class AstPrinter(Expr.Visitor):

    def print_expr(self, expr):

        return expr.accept(self)
    
    def visit_binary_expr(self, expr):

        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_grouping_expr(self, expr):

        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):

        if expr.value is None:
            return "nil"

        return str(expr.value)
    
    def visit_unary_expr(self, expr):

        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs):
        
        name = "(" + name 

        for expr in exprs:
            name = name + " " + expr.accept(self) 
        
        name = name + ")"

        return name

    @staticmethod
    def main(args: list[str]):

        expression = Binary(Unary
                            (Token(TokenType.MINUS, "-", None, 1),
                                  Literal(123)
                             ),
                            Token(TokenType.STAR, "*", None, 1),
                            Grouping(Literal(45.67)
                            )
                    )

        print(AstPrinter().print_expr(expression))

if __name__=="__main__":
    AstPrinter.main([])





