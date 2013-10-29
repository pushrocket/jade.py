import re
from . token import Token

class Lexer(object):
  """Lexer class"""

  def __init__(self, str, options = {}):
    """
    Initialize `Lexer` with the given `str`.
    Options:
      `colons` allow colons for attr delimiter
    """
    options = options or {}
    self.input = re.sub('\r\n|\r', '\n', str)
    self.colons = 'colons' in options.keys() and options['colons']
    self.deferred_tokens = []
    self.last_indents = 0
    self.lineno = 1
    self.stash = []
    self.indent_stack = []
    self.indentRe = None
    self.pipeless = False

  def tok(self, type, val = None):
    ''' Construct a Token with the given `type` and `val`.

    :param type: string
    :param val: string
    :returns: a token
    '''
    return Token(type, val, self.lineno)

  def consume(self, len):
    ''' Consume the given `len` of input.

    :param len: number of chars to consume
    '''
    self.input = self.input[len:]

  def scan(self, regex, type):
    ''' Scan for `type` with the given `regex`.

    :param type: string
    :param regex: re
    :returns: a `Token` if regex matches
    '''
    matches = regex.match(self.input)

    if matches is not None:
      match = matches.group(0)
      self.consume(len(match))
      return self.tok(type, matches.group(1))

  def lookahead(self, n):
    ''' Look ahead `n` tokens

    :param n: number of items to lookahead
    :retuns: the next token
    '''
    fetch = n - len(self.stash)

    while fetch > 0:
      self.stash.append(self.next())
      fetch = fetch - 1

    return self.stash[n - 1]

  def advance(self):
    ''' Return the next token object, or those previously stashed by lookahead.

    :returns: a token
    '''

    return self.stashed() or self.next()

  def stashed(self):
    ''' Remove and return any stashed tokens '''

    if len(self.stash) is 0:
      return None

    return self.stash.pop(0)

  def next(self):
    ''' The next token.

    :returns: the next token
    '''
    token = self.eos() \
      or self.tag() \
      or self.text()

    print('lexed: ' + token.type)

    return token

  def eos(self):
    ''' End Of Source '''

    if len(self.input) > 0:
      return

    if len(self.indent_stack) > 0:
      self.indent_stack.pop(0);
      return self.tok('outdent')
    else:
      return self.tok('eos')

  no_space_text_re = re.compile('^([^\.\<][^\n]+)')
  inline_text_re = re.compile('^(?:\| ?| )([^\n]+)')
  multiline_text_re = re.compile('^([^\.][^\n]+)')

  def text(self):
    if Lexer.no_space_text_re.match(self.input) and not Lexer.inline_text_re.match(self.input):
      raise Warning('Warning: missing space before text for line ' + self.lineno + ' of jade file.')
    return self.scan(Lexer.inline_text_re, 'text') or self.scan(Lexer.multiline_text_re,'text');

  tag_re = re.compile('^(\w[-:\w]*)(\/?)')
  def tag(self):
    ''' Returns a tag if matches. Else `None` '''
    matches = Lexer.tag_re.match(self.input)

    if matches is not None:
      name = matches.group(1)
      tok = None
      self.consume(len(name))

      if name[-1] == ':': # ends with colon?
        name = name[0:-1] # remove the last char
        tok = self.tok('tag', name)
        self.defer(self.tok(':'))

        while self.input[0] == ' ':
          self.input = self.input[1:] # remove first char

      else:
        tok = self.tok('tag', name)

      tok.self_closing = matches.group(2) is '/'

      return tok