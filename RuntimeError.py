class RuntimeError(RuntimeError):
  """ Custom RuntimeError with error info of supplied token.

  Args:
      RuntimeError (_type_): _description_
  """
  def __init__(self, token = None, *args: object) -> None:
    super().__init__(*args)
    self.message = args
    self.token = token