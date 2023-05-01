import expr
import stmt
import environment as env
from RuntimeError import RuntimeError
import gelic
from TokenType import TokenType
from Token import Token

class Interpreter(expr.Visitor, stmt.Visitor):
  
  def __init__(self, gelic) -> None:
    super().__init__()
    self.environment : env.Environment = env.Environment()
    self.gelic = gelic
    
  def interpret(self, statements : list[stmt.Stmt]):
    try:
      for statement in statements:
        self.__execute(statement)
    except RuntimeError as err:
       self.gelic.runtimeError(err)

  # ============= OVERRIDES ============= #
   
  def visitLiteralExpr(self, expr : expr.Literal):
    return expr.value
  
  def visitLogicalExpr(self, expr : expr.Logical):
    left = self.__evaluate(expr.left)
    
    if expr.operator.type == TokenType.OR:
      if self.__isTruthy(left): return left
    else: 
      if not self.__isTruthy(left): return left
      
    return self.__evaluate(expr.right)
  
  
  def visitGroupingExpr(self, expr : expr.Grouping):
    return self.__evaluate(expr.expression)
  
  def visitUnaryExpr(self, expr : expr.Unary):
    right = self.__evaluate(expr.right)
    
    match expr.operator.type:
      case TokenType.BANG:
        return self.__isTruthy(right)
      case TokenType.MINUS:
        self.__checkNumberOperand(expr.operator, right)
        return -float(right)

    # Unreachable
    return None
  
  def visitBinaryExpr(self, expr: expr.Binary):
    left = self.__evaluate(expr.left)
    right = self.__evaluate(expr.right)
    
    match expr.operator.type:
      case TokenType.GREATER:
        self.__checkNumberOperands(expr.operator, left, right)
        return float(left) > float(right)
      
      case TokenType.GREATER_EQUAL:
        self.__checkNumberOperands(expr.operator, left, right)
        return float(left) >= float(right)
      
      case TokenType.LESS:
        self.__checkNumberOperands(expr.operator, left, right)
        return float(left) < float(right)
      
      case TokenType.LESS_EQUAL:
        self.__checkNumberOperands(expr.operator, left, right)
        return float(left) <= float(right)
      
      case TokenType.BANG_EQUAL:
        return not self.__isEqual(left, right)
      
      case TokenType.EQUAL_EQUAL:
        return self.__isEqual(left, right)
      
      case TokenType.MINUS:
        return float(left) - float(right)
      
      case TokenType.PLUS:
        if isinstance(left, float) and isinstance(right, float):
          return float(left) + float(right)
        
        if isinstance(left, str) and isinstance(right, str):
          return str(left) + str(right)
        
        raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
      
      case TokenType.SLASH:
        self.__checkNumberOperands(expr.operator, left, right)
        return float(left) / float(right)
      
      case TokenType.STAR:
        self.__checkNumberOperands(expr.operator, left, right)
        return float(left) * float(right)
      
    # Unreachable
    return None
  
  # ============================ #
  
  def __checkNumberOperand(self, operator : Token, operand : object):
    if isinstance(operand, float): return
    
    raise RuntimeError(operator, "Operand must be a number.")
  
  def __checkNumberOperands(self, operator : Token, left : object, right : object):
    if isinstance(left, float) and isinstance(right, float): return
    
    raise RuntimeError(operator, "Operands must be numbers.")
  
  def __isTruthy(self, obj : object) -> bool:
    """ False and nil are false values. Everything else is true.

    Args:
        obj (object): _description_

    Returns:
        bool: _description_
    """
    
    if obj == None: return False
    
    if isinstance(obj, bool): return bool(obj)
    
    return True
  
  def __isEqual(self, a : object, b : object) -> bool:
    if a == None and b == None: return True
    if a == None: return False
    
    return a == b
  
  def __stringify(self, obj : object) -> str:
    if obj == None: return "nil"
    
    if isinstance(obj, float):
      text : str = str(obj)
      if text[-2:] == ".0":
        text = text[0 : len(text)-2]
      return text
    
    return str(obj)
  
  def __evaluate(self, expr : expr.Expr):
    return expr.accept(self)
  
  def __execute(self, stmt: stmt.Stmt):
    stmt.accept(self)
    
  def executeBlock(self, statements: list[stmt.Stmt], environment : env.Environment):
    previous : env.Environment =  self.environment
    
    try:
      self.environment = environment
      
      for statement in statements:
        self.__execute(statement)
    finally:
      self.environment = previous
      
  # ============== OVERRIDES ============= #
  
  def visitBlockStmt(self, stmt : stmt.Block):
    self.executeBlock(stmt.statements, env.Environment(self.environment))
    return None
  
  def visitExpressionStmt(self, stmt : stmt.Expression):
    self.__evaluate(stmt.expression)
    return None
  
  def visitIfStmt(self, stmt : stmt.If):
    if self.__isTruthy(self.__evaluate(stmt.condition)):
      self.__execute(stmt.thenBranch)
    elif stmt.elseBranch != None:
      self.__execute(stmt.elseBranch)
    
    return None
  
  def visitPrintStmt(self, stmt : stmt.Print):
    value : object = self.__evaluate(stmt.expression)
    print(self.__stringify(value))
    return None
    
  def visitVarStmt(self, stmt : stmt.Var):
    value: object = None
    if stmt.initializer != None:
      value = self.__evaluate(stmt.initializer)
      
    self.environment.define(stmt.name.lexeme, value)
    return None
  
  # ========================================= #
  
  def visitWhileStmt(self, stmt : stmt.While):
    while self.__isTruthy(self.__evaluate(stmt.condition)):
      self.__execute(stmt.body)
      
    return None

  def visitAssignExpr(self, expr : expr.Assign):
    value: object = self.__evaluate(expr.value)
    self.environment.assign(expr.name, value)
    return value
  
  def visitVariableExpr(self, expr : expr.Variable):
    return self.environment.get(expr.name)