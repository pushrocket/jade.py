from . node import Node

class Text(Node):

  def __init__(self, val):
    ''' Initialize a `Text` node with optional `val`

    :param line: line of text
    '''

    self._is_text = True
    self._val = ''

    if isinstance(val, str):
      self._val = val

  @property
  def is_text(self):
      return self._is_text

  @is_text.setter
  def is_text(self, value):
      self._is_text = value

  @property
  def val(self):
      return self._val

  @val.setter
  def val(self, value):
      self._val = value
