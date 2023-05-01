from abc import ABC, abstractmethod
from expr import Expr
from Token import Token
import stmt 

class Visitor(ABC):
  
  @abstractmethod
  def visitBlockStmt(stmt): pass
  
  @abstractmethod
  def visitExpressionStmt(stmt): pass
  
  @abstractmethod
  def visitIfStmt(stmt): pass
  
  @abstractmethod
  def visitPrintStmt(stmt): pass
  
  @abstractmethod
  def visitVarStmt(stmt): pass
  
  @abstractmethod
  def visitWhileStmt(stmt): pass

class Stmt(ABC):
  @abstractmethod
  def accept(visitor: Visitor): pass
  
  
class Block(Stmt):
  def __init__(self, statements) -> None:
    super().__init__()
    self.statements = statements
  
  def accept(self, visitor: Visitor):
    return visitor.visitBlockStmt(self)   
  
class Expression(Stmt):
  def __init__(self, expression : Expr) -> None:
    super().__init__() 
    self.expression = expression
  
  def accept(self, visitor: Visitor):
    return visitor.visitExpressionStmt(self)
  
class If(Stmt):
  def __init__(self, condition : Expr, thenBranch: Stmt, elseBranch: Stmt) -> None:
    super().__init__()
    self.condition = condition
    self.thenBranch = thenBranch
    self.elseBranch = elseBranch
    
  def accept(self, visitor: Visitor):
    return visitor.visitIfStmt(self)
  
class Print(Stmt):
  def __init__(self, expression : Expr) -> None:
    super().__init__()
    self.expression = expression
  
  def accept(self, visitor: Visitor):
    return visitor.visitPrintStmt(self)
  
class Var(Stmt):
  def __init__(self, name : Token, initializer : Expr) -> None:
    super().__init__()
    self.name = name
    self.initializer = initializer
    
  def accept(self, visitor: Visitor):
    return visitor.visitVarStmt(self)
  
class While(Stmt):
  def __init__(self, condition: Expr, body : Stmt) -> None:
    super().__init__()
    self.condition = condition
    self.body = body
    
  def accept(self, visitor: Visitor):
    return visitor.visitWhileStmt(self)