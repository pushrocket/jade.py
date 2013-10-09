import lib.nodes as nodes
from . lexer import Lexer

# Tags that may not contain tags.
textOnly = ['script', 'style'];

class Parser(object):
  '''Parser class'''

  def __init__(self, str, filename, options):
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
    pass

  def skip(self, n):
    pass

  def peek(self):
    pass

  def line(self):
    pass

  def lookahead(self, n):
    pass

  def parse(self):
    block = nodes.Block()
    block.line = self.line()

    # while ('eos' != this.peek().type) {
    #   if ('newline' == this.peek().type) {
    #     this.advance();
    #   } else {
    #     block.push(this.parseExpr());
    #   }
    # }

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

