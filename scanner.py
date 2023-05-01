from Token import Token
from typing import List, TypeVar
from TokenType import *
import gelic

# AKA lexer
class Scanner:
  
  keywords = {
    "and" : TokenType.AND,
    "class" : TokenType.CLASS,
    "else" : TokenType.ELSE,
    "false" : TokenType.FALSE,
    "for" : TokenType.FOR,
    "fun" : TokenType.FUN,
    "if" : TokenType.IF,
    "nil" : TokenType.NIL,
    "or" : TokenType.OR,
    "print" : TokenType.PRINT,
    "return" : TokenType.RETURN,
    "super"  : TokenType.SUPER,
    "this"   : TokenType.THIS,
    "true"   : TokenType.TRUE,
    "var"   : TokenType.VAR,
    "while" : TokenType.WHILE
  }
  
  def __init__(self, source : str, gelic) -> None:
    self.source = source
    self.tokens = []
    self.start = 0
    self.current = 0
    self.line = 1
    self.gelic = gelic
    
  def scanTokens(self) -> List:
    while not self.__isAtEnd():
      self.start = self.current
      self.scanToken()
      
    self.tokens.append(Token(TokenType.EOF, "", None, self.line))
    return self.tokens
  
  def scanToken(self):
    c  = self.__advance()
    
    match c:
      case "(":
        self.__addToken(TokenType.LEFT_PAREN)
      case ")":
        self.__addToken(TokenType.RIGHT_PAREN)
      case "{":
        self.__addToken(TokenType.LEFT_BRACE)
      case "}":
        self.__addToken(TokenType.RIGHT_BRACE)
      case ",":
        self.__addToken(TokenType.COMMA)
      case ".":
        self.__addToken(TokenType.DOT)
      case "-":
        self.__addToken(TokenType.MINUS)
      case "+":
        self.__addToken(TokenType.PLUS)
      case ";":
        self.__addToken(TokenType.SEMICOLON)
      case "*":
        self.__addToken(TokenType.STAR)
      case "!":
        self.__addToken(TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG)
      case "=":
        self.__addToken(TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL)
      case "<":
        self.__addToken(TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS)
      case ">":
        self.__addToken(TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER)
      case "/":
        if self.__match("/"):
          # A comment goes until the end of the line.
          while self.__peek() != "\n" and not self.__isAtEnd():
            self.__advance()
        else:
          self.__addToken(TokenType.SLASH)
      case '"':
        self.__string()
      case " " | "\r" | "\t":
        return
      case "\n":
        self.line += 1
      case _:
        if self.__isDigit(c):
          self.__number()
        elif self.__isAlpha(c):
          self.__identifier()
        else:
          self.gelic.error(self.line, "Unexpected character.")
          
  def __identifier(self) -> None:
    while self.__isAlphaNumeric(self.__peek()): self.__advance()
    
    text : str = self.source[self.start : self.current]
    type : TokenType = Scanner.keywords.get(text)
    
    if type == None:
      type = TokenType.IDENTIFIER
      
    self.__addToken(type)

  def __number(self) -> None:
    while self.__isDigit(self.__peek()): 
      self.__advance()
    
    # look for a fractional part
    if self.__peek() == "." and self.__isDigit(self.__peekNext()):
      # consume the .
      self.__advance()
      
      while self.__isDigit(self.__peek()):
        self.__advance()
    
    self.__addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))
        
  def __string(self) -> None:
    while self.__peek() != '"' and not self.__isAtEnd():
      if self.__peek() == "\n": 
        self.line += 1
      self.__advance()
    
    if self.__isAtEnd():
      gelic.Gelic.error(self.line, "Unterminated string.")
      return

    # Closing "
    self.__advance()
    
    # Trim surrounding quotes
    value : str = self.source[self.start + 1 : self.current - 1]
    self.__addToken(TokenType.STRING, value)
        
  def __match(self, expected : chr) -> bool:
    if self.__isAtEnd(): return False
    if self.source[self.current] != expected: return False
    
    self.current += 1
    return True
  
  def __peek(self) -> chr:
    if self.__isAtEnd(): return "\0"
    return self.source[self.current]
  
  def __peekNext(self) -> chr : 
    if self.current + 1 >= len(self.source): return "\0"
    
    return self.source[self.current + 1]
  
  def __isAlphaNumeric(self, c):
    return self.__isAlpha(c) or self.__isDigit(c)
  
  def __isAlpha(self, c : chr) -> bool:
    return (
      (c >= "a" and c <= "z") or
      (c >= "A" and c <= "Z") or 
      c == "_" 
    )
  
  def __isDigit(self, c : chr) -> bool:
    return c >= "0" and c <= "9"
            
  def __addToken(self, type):
    self.__addToken(type, None)
  
  def __addToken(self, type, literal = None):
    text = self.source[self.start : self.current]
    self.tokens.append(Token(type, text, literal, self.line))
    
  def __advance(self) -> chr :
    """ Consumes the next character in the source file and returns it.

    Returns:
        chr: The next character
    """
    curr = self.current

    self.current += 1

    return self.source[curr]
  
  
  def __isAtEnd(self) -> bool:
    return self.current >= len(self.source)
  