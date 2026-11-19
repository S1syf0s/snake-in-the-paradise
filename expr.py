from dataclasses import dataclass
from snake_token import Token

class Expr:
    pass

@dataclass
class Assing(Expr):
    name: Token
    value: Expr

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Literal(Expr):
    value: object

@dataclass
class Conditional(Expr):
    condition: Expr
    then_branch: Expr
    else_branch: Expr

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass
class Variable(Expr):
    name: Token

