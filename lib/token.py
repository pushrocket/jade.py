class Token(object):

  def __init__(self, type, val, line):
    self._type = type
    self._val = val
    self._line = line
    self._self_closing = False

  @property
  def type(self):
    return self._type

  @property
  def val(self):
    return self._val

  @property
  def line(self):
    return self._line

  @property
  def self_closing(self):
    return self._self_closing

  @self_closing.setter
  def self_closing(self, value):
    self._self_closing = value

  @property
  def type(self):
      return self._type
  @type.setter
  def type(self, value):
      self._type = value

