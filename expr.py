from abc import ABC, abstractmethod
from Token import Token


class Visitor(ABC):
  
  @abstractmethod
  def visitAssignExpr(expr):
    pass

  @abstractmethod
  def visitBinaryExpr(expr):
    pass

  @abstractmethod
  def visitGroupingExpr(expr):
    pass
  
  @abstractmethod
  def visitLiteralExpr(expr):
    pass
  
  @abstractmethod
  def visitLogicalExpr(expr):
    pass
  
  @abstractmethod
  def visitUnaryExpr(expr):
    pass
  
  @abstractmethod
  def visitVariableExpr(expr):
    pass


class Expr(ABC):
  
  @abstractmethod
  def accept(self, visitor : Visitor):
    pass
  
class Assign(Expr):
  def __init__(self, name : Token, value : Expr) -> None:
    super().__init__()
    self.name = name
    self.value = value
    
  def accept(self, visitor : Visitor):
    return visitor.visitAssignExpr(self)

class Binary(Expr):
  def __init__(self, left : Expr, operator : Token, right : Expr) -> None:
    super().__init__()
    self.left = left
    self.operator = operator
    self.right = right

  def accept(self, visitor : Visitor):
    return visitor.visitBinaryExpr(self)

class Grouping(Expr):
  def __init__(self, expression : Expr) -> None:
    super().__init__()
    self.expression = expression
    
  def accept(self, visitor : Visitor):
    return visitor.visitGroupingExpr(self)
    
class Literal(Expr):
  
  def __init__(self, value : object) -> None:
    super().__init__()
    self.value = value
    
  def accept(self, visitor : Visitor):
    return visitor.visitLiteralExpr(self)

class Logical(Expr):
  def __init__(self, left : Expr, operator : Token, right: Expr) -> None:
    super().__init__()
    self.left = left
    self.operator = operator
    self.right = right
    
  def accept(self, visitor: Visitor):
    return visitor.visitLogicalExpr(self)    

class Unary(Expr):
  def __init__(self, operator : Token, right : Expr) -> None:
    super().__init__()
    self.operator = operator
    self.right = right
    
  def accept(self, visitor: Visitor):
    return visitor.visitUnaryExpr(self)
    
class Variable(Expr):
  def __init__(self, name : Token) -> None:
    super().__init__()
    self.name = name
    
  def accept(self, visitor: Visitor):
    return visitor.visitVariableExpr(self)