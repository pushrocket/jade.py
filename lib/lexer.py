import re

class Lexer(object):
  """Lexer class"""

  def __init__(self, str, options):
    """
    Initialize `Lexer` with the given `str`.
    Options:
      `colons` allow colons for attr delimiter
    """
    options = options or {}
    self.input = re.sub('\r\n|\r', '\n', str)
    self.colons = options.colons
    self.deferredTokens = []
    self.lastIndents = 0
    self.lineno = 1
    self.stash = []
    self.indentStack = []
    self.indentRe = None
    self.pipeless = False

  def lookahead(self, n):
    """Look ahead `n` tokens"""
    fetch = n - self.stash.length

    while fetch > 0:
      self.stash.append(self.next())
      fetch = fetch - 1

    return self.stash[n - 1]

  def next(self):
    return self.tag()