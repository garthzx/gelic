import TokenType

class Token:
  def __init__(self, type : TokenType, lexeme : str, literal : object, line : int) -> None:
    self.type = type
    self.lexeme = lexeme
    self.literal = literal
    self.line = line
    
  def toString(self):
    return f"{self.type} {self.lexeme} {self.literal}"
    
  