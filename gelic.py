import sys
from tools.bcolors import *
import scanner as sc
from Token import Token
import interpreter as itpr
import gparser as gp
from TokenType import TokenType
from RuntimeError import RuntimeError

class Gelic:
  """ 
  @author Garth Ayang-ang
  """
  
  def __init__(self) -> None:
    self.interpreter = itpr.Interpreter(self)  
    self.hadError = False
    self.hadRuntimeError = False
      
  def runPrompt(self):
    interpreter = itpr.Interpreter(self)
    while True:
      print("> ", end="")
      line = str(input())
      if line == None: break
      self.run(line, interpreter)
      self.hadError = False
      
  def runFile(self, path):
    with open(path, "r") as in_file:
      source = in_file.read()
      # print(source)
    
    interpreter = itpr.Interpreter(self)
    self.run(str(source), interpreter)
    if self.hadError: sys.exit(5)
    if self.hadRuntimeError: sys.exit(70)

  def run(self, source, interpreter):
    scanner = sc.Scanner(source, self)
    tokens = scanner.scanTokens()

    # for token in tokens:
    #   print(token.toString())      

    # gelic = Gelic()
    parser = gp.Parser(tokens, self)
    
    statements = parser.parse()
    
    # Do not continue to interpreter.
    if self.hadError:
      return
        
    interpreter.interpret(statements)
    
  def error(self, line, message):
    self.report(line, "", message)
    
  def errorWithToken(self, token : Token, message : str):
    if token.type == TokenType.EOF:
      self.report(token.line, " at end", message)
    else:
      self.report(token.line, f" at '{token.lexeme}'", message)
  
  def runtimeError(self, error : RuntimeError):
    print(f"{bcolors.FAIL}{error.message[0]} \n[line {error.token.line}]{bcolors.ENDC}")
    self.hadRuntimeError = True
    
  def report(self, line, where, message):
    print(f"{bcolors.FAIL}[line {line}] Error{where}: {message}{bcolors.ENDC}")
    self.hadError = True

  def main(self):
    args = sys.argv
    # print(len(args))
    if len(args) > 2:
      print(bcolors.FAIL + "Usage: python3 Gelic.py [/pathto/script.txt]" + bcolors.ENDC)
      sys.exit(64)
    elif len(args) == 2:
      self.runFile(args[1])
    else:
      self.runPrompt()  

if __name__ == "__main__":
  Gelic().main()