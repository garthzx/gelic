import expr
import stmt
from Token import Token
from TokenType import TokenType

class AstPrinter(expr.Visitor):
  
  def print(self, expr : expr.Expr):
    return str(expr.accept(self))
  
  def visitAssignExpr(expr):
    return None
  
  def visitBinaryExpr(self, expr : expr.Binary):
    return str(self.parenthesize(name=expr.operator.lexeme, exprs = [expr.left, expr.right]))
  
  def visitGroupingExpr(self, expr : expr.Grouping):
    return str(self.parenthesize(name="group", exprs=[expr.expression]))
  
  def visitLiteralExpr(self, expr : expr.Literal):
    if expr.value == None: return "nil"
    #TODO:
    return str(expr.value)
    # return expr.value.toString()
  
  #TODO:
  def visitLogicalExpr(expr):
    return super().visitLogicalExpr()
  
  def visitUnaryExpr(self, expr : expr.Unary):
    return str(self.parenthesize(name=expr.operator.lexeme, exprs=[expr.right]))
  
  #TODO:
  def visitVariableExpr(expr):
    return super().visitVariableExpr()
  
  def parenthesize(self, name : str, exprs : list):
    build = ""
    build += f"({name}"
    for expr in exprs:
      build += " "
      build += str(expr.accept(self))
      
    build += ")"
    
    return build
  
  
if __name__ == "__main__":
  expression : expr.Expr = expr.Binary(
    expr.Unary(
      Token(TokenType.MINUS, "-", None, 1),
      expr.Literal(123)),
    
    Token(TokenType.STAR, "*", None, 1),
    expr.Grouping(
      expr.Literal(45.67)
    )
  )
  
  print(AstPrinter().print(expression))