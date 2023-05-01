from __future__ import annotations
from Token import Token
from RuntimeError import RuntimeError

class Environment:

  def __init__(self, enclosing : Environment = None) -> None:
    self.enclosing = enclosing
    self.values = {}
      
  def get(self, name : Token) -> object:
    """Returns the value bound to name.lexeme. Otherwise, throw a RuntimeError. 

    Args:
        name (Token): key

    Raises:
        RuntimeError: Undefined variable.

    Returns:
        object: The value look up.
    """
    if name.lexeme in self.values.keys():
      return self.values.get(name.lexeme)

    if self.enclosing != None: 
      return self.enclosing.get(name)

    raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
  
  
  def assign(self, name: Token, value: object):
    """ Does not allow creation of a new variable. A RuntimeError is thrown
        if the key does not exist in the environment's map.

    Args:
        name (Token): The key to be assigned
        value (object): Value for key name

    Raises:
        RuntimeError: Undefined variable
    """
    if name.lexeme in self.values.keys():
      self.values[name.lexeme] = value
      return

    if self.enclosing != None:
      self.enclosing.assign(name, value)
      return
    
    raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
  
  def define(self, name : str, value: object):
    """ Binds a new name to value. It performs no checking if it's already present.
        This can be used to redefine an existing variable.
        For example:
          var a = "before";
          print a; // before
          var a = "after";
          print a; // after

    Args:
        name (str): _description_
        value (object): _description_
    """
    self.values[name] = value