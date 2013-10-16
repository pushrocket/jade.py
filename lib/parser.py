import re
import lib.nodes as nodes
from . lexer import Lexer
from . doctypes import doctypes

# Tags that may not contain tags.
textOnly = ['script', 'style'];

class Parser(object):
  '''Parser class'''

  def __init__(self, str, filename, options = {}):
    '''Initialize `Parser` with the given input `str` and `filename`'''

    # Strip any UTF-8 BOM off of the start of `str`, if it exists.
    self.input = re.sub('^\uFEFF', '', str)
    self.lexer = Lexer(self.input, options);
    self.filename = filename;
    self.blocks = {};
    self.mixins = {};
    self.options = options;
    self.contexts = [self];
    self.extending = None

  def context(self, parser):
    '''Push `parser` onto the context stack, or pop and return a `Parser`.'''

    if parser is not None:
      self.contexts.append(parser)
    else:
      return self.contexts.pop()

  def advance(self):
    return self.lexer.advance()

  def skip(self, n):
    pass

  def peek(self):
    return self.lookahead(1)

  def line(self):
    pass

  def lookahead(self, n):
    return self.lexer.lookahead(n)

  def parse(self):
    block = nodes.Block()
    block.line = self.line()

    while 'eos' != self.peek().type:
      if 'newline' == self.peek().type:
        self.advance()
      else:
        block.push(self.parse_expr());

    if self.extending is not None:
      parser = self.extending
      self.context(parser) # push
      ast = parser.parse()
      self.context() # pop

      # hoist mixins
      for key in self.mixins.keys():
        ast.unshift(self.mixins[key])
      return ast

    return block;

  def expect(self, type):
    ''' Expect the given type, or throw an exception.

    :param type:
    @api private
    '''

    if self.peek().type is type:
      return self.advance()
    else:
      raise Exception('expected "' + type + '", but got "' + self.peek().type + '"')

  def parse_expr(self):
    type = self.peek().type

    if type is 'tag':
      return self.parse_tag();

  def parse_text(self):
    ''' Creates a Text node from tne next token '''

    tok = self.expect('text')
    node = nodes.Text(tok.val)
    node.line = self.line()
    return node

  def parse_tag(self):
    ''' tag (attrs | class | id)* (text | code | ':')? newline* block? '''

    # ast-filter look-ahead
    i = 2;
    if 'attrs' == self.lookahead(i).type:
      i = i + 1

    tok = self.advance()
    tag = nodes.Tag(tok.val)

    tag.self_closing = tok.self_closing

    return self.tag(tag)

  def tag(self, tag):
    tag.line = self.line()

    seen_attr = False
    peek_type = self.peek().type

    if peek_type is 'text':
      tag.block.push(self.parse_text())

    return tag
