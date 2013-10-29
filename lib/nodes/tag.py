from . attrs import Attrs
from . block import Block
from .. inlineTags import inline_tags
# from . text import Text

class Tag(Attrs):

  def __init__(self, name, block = None):
    '''Initialize a `Tag` node with the given tag `name` and optional `block`.'''

    self.name = name
    self.attrs = []
    self.block = block or Block()
    self.text_only = False
    self._self_closing = False

  def clone(self):
    '''Clone this tag'''

    c = Tag(self.name, self.block.clone())
    c.line = self.line
    c.attrs = self.attrs.copy()
    c.text_only = self.text_only

  def is_inline(self):
    '''Check if this tag is an inline tag'''

    return self.name in inlineTags

  def can_inline(self):
    '''Check if this tag's contents can be inlined.  Used for pretty printing.'''

    nodes = self.block.nodes

    def is_inline(node):
      if node.is_block:
        return all([is_inline(n) for n in node.nodes])

      return (hasattr(node, 'is_text') and node.is_text) or (hasattr(node, 'is_inline') and node.is_inline())

    # empty tag
    if len(nodes) is 0:
      return true

    # text-only or inline-only tag
    if len(nodes) is 1:
      return is_inline(nodes[0])

    # Multi-line inline-only tag
    if all([is_inline(n) for n in node.nodes]):
      for i in range(1, len(nodes)):
        previous = nodes[i-1]
        node = nodes[i]

        if hasattr(previous, 'is_text') and previous.is_text and hasattr(node, 'is_text') and node.is_text:
          return False

      return True

    # mixed tag
    return False

  @property
  def self_closing(self):
    return self._self_closing

  @self_closing.setter
  def self_closing(self, value):
    self._self_closing = value
