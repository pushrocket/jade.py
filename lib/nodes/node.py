class Node(object):
  def __init__(self):
    self._line = None

  def clone(self):
    return self

  @property
  def line(self):
      return self._line

  @line.setter
  def line(self, value):
      self._line = value
