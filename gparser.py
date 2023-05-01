from Token import Token
from TokenType import TokenType
from stmt import *
from expr import *
from RuntimeError import RuntimeError
import gelic

class ParseError(RuntimeError):
  pass

class Parser:
  
  def __init__(self, tokens: list[Token], gelic) -> None:
    self.tokens = tokens
    self.current = 0
    self.gelic = gelic
    
  def parse(self) -> list[Stmt]:
    statements = []
    
    while not self.__isAtEnd():
      statements.append(self.__declaration())
    
    return statements
  
  def __declaration(self) -> Stmt:
    try:
      if self.__match(TokenType.VAR): return self.__varDeclaration()
      return self.__statement()
    except ParseError as pe:
      self.__synchronize()
      return None
    
  def __expression(self) -> Expr:
    return self.__assignment()
  
  def __statement(self) -> Stmt:
    if self.__match(TokenType.FOR): return self.__forStatement()
    if self.__match(TokenType.IF): return self.__ifStatement()
    if self.__match(TokenType.PRINT): return self.__printStatement()
    if self.__match(TokenType.WHILE): return self.__whileStatement()
    if self.__match(TokenType.LEFT_BRACE): return Block(self.__block())
    
    return self.__expressionStatement()
  
  def __forStatement(self) -> Stmt:
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
    
    initializer : Stmt = None
    
    if self.__match(TokenType.SEMICOLON):
      initializer = None
    elif self.__match(TokenType.VAR):
      initializer = self.__varDeclaration()
    else:
      initializer = self.__expressionStatement()
      
    condition : Expr = None
    
    if not self.__check(TokenType.SEMICOLON):
      condition = self.__expression()
      
    self.__consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
      
    increment: Expr = None
    if not self.__check(TokenType.RIGHT_PAREN):
      increment = self.__expression()
      
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
    
    body : Stmt = self.__statement()
    
    # De-sugaring
    if increment != None:
      body = Block([
        body, Expression(increment)
      ])
    
    if condition == None:
      condition = Literal(True)
    
    body = While(condition, body)
    
    if initializer != None:
      body = Block([initializer, body])    
    
    return body
  
  def __ifStatement(self) -> Stmt:
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
    condition : Expr = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
    
    thenBranch : Stmt = self.__statement()
    elseBranch : Stmt = None
    
    if self.__match(TokenType.ELSE): 
      elseBranch = self.__statement()

    return If(condition, thenBranch, elseBranch)
  
  def __printStatement(self) -> Stmt:
    value : Expr = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after value")
    return Print(value)
  
  def __varDeclaration(self) -> Stmt:
    name : Token = self.__consume(TokenType.IDENTIFIER, "Expect variable name.")
    
    initializer : Expr = None
    if self.__match(TokenType.EQUAL):
      initializer = self.__expression()
      
    self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
    return Var(name, initializer)
  
  def __whileStatement(self) -> Stmt:
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after whlie.")
    condition : Expr = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after condition")
    body : Stmt = self.__statement()
    
    return While(condition, body)
  
  
  def __expressionStatement(self) -> Stmt:
    expr : Expr = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after epxression")
    return Expression(expr)
  
  def __block(self) -> list[Stmt] :
    statements : list[Stmt] = []
    
    while not self.__check(TokenType.RIGHT_BRACE) and not self.__isAtEnd():
      statements.append(self.__declaration())
    
    self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
    return statements
  
  def __assignment(self) -> Expr:
    expr : Expr = self.__or()
    
    if self.__match(TokenType.EQUAL):
      equals : Token = self.__previous()
      value : Expr = self.__assignment()
      
      if isinstance(expr, Variable):
        name : Token = expr.name
        return Assign(name, value)
      
      self.__error(equals, "Invalid assignment target.")
      
    return expr
  
  def __or(self) -> Expr:
    expr : Expr = self.__and()
    
    while self.__match(TokenType.OR):
      operator : Token = self.__previous()
      right : Expr = self.__and()
      expr = Logical(expr, operator, expr)
    
    return expr
  
  def __and(self) -> Expr :
    expr : Expr = self.__equality()
    
    while self.__match(TokenType.AND):
      operator = self.__previous()
      right = self.__equality()
      expr = Logical(expr, operator, right)
    
    return expr
  
  def __equality(self) -> Expr:
    expr : Expr = self.__comparison()
    
    while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator = self.__previous()
      right = self.__comparison()
      expr = Binary(expr, operator, right)
    
    return expr
  
  def __comparison(self) -> Expr:
    expr : Expr = self.__term()
    
    while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
      operator : Token = self.__previous()
      right : Expr = self.__term()
      expr = Binary(expr, operator, right)
    
    return expr
  
  def __term(self) -> Expr:
    expr : Expr = self.__factor()
    
    while self.__match(TokenType.MINUS, TokenType.PLUS):
      operator = self.__previous()
      right = self.__factor()
      expr = Binary(expr, operator, right)
      
    return expr
  
  def __factor(self) -> Expr:
    expr : Expr = self.__unary()
    
    while self.__match(TokenType.SLASH, TokenType.STAR):
      operator = self.__previous()
      right = self.__unary()
      expr = Binary(expr, operator, right)
      
    return expr
  
  def __unary(self) -> Expr:
    if self.__match(TokenType.BANG, TokenType.MINUS):
      operator = self.__previous()
      right = self.__unary()
      return Unary(operator, right)
    
    return self.__primary()
  
  def __primary(self) -> Expr:
    if self.__match(TokenType.FALSE): return Literal(False)
    if self.__match(TokenType.TRUE): return Literal(True)
    if self.__match(TokenType.NIL): return Literal(None)
    
    if self.__match(TokenType.NUMBER, TokenType.STRING):
      return Literal(self.__previous().literal)
    
    if self.__match(TokenType.IDENTIFIER):
      return Variable(self.__previous())
    
    # When ( is matched, find ) token.
    if self.__match(TokenType.LEFT_PAREN):
      expr = self.__expression()
      self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
      return Grouping(expr)
    
    raise self.__error(self.__peek(), "Expect expression")
  
  ######## PRIMITIVE OPERATIONS ############
  
  def __match(self, *types : list[TokenType]) -> bool:
    for type in types:
      if self.__check(type):
        self.__advance()
        return True
      
    return False

  def __consume(self, type : TokenType, message : str) -> Token:
    if self.__check(type): return self.__advance()
    
    raise self.__error(self.__peek(), message)
  
  def __error(self, token : Token, message : str) -> ParseError:
    self.gelic.errorWithToken(token, message)
    return ParseError()
  
  def __synchronize(self):
    self.__advance()
    
    while not self.__isAtEnd():
      if self.__previous().type == TokenType.SEMICOLON: return
      
      match self.__peek().type:
        case TokenType.CLASS |TokenType.FUN | TokenType.VAR | TokenType.FOR | \
          TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN:
            return
      self.__advance()
      
  def __check(self, type : TokenType) -> bool:
    if self.__isAtEnd(): return False
    
    return self.__peek().type == type
  
  def __advance(self) -> TokenType:
    if not self.__isAtEnd(): self.current += 1
    
    return self.__previous()
  
  def __isAtEnd(self) -> bool:
    return self.__peek().type == TokenType.EOF
  
  def __peek(self) -> Token:
    return self.tokens[self.current]
  
  def __previous(self) -> Token:
    return self.tokens[self.current - 1]