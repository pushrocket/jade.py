from . attrs import Attrs
from . block import Block
from .. inlineTags import inlineTags
# from . text import Text

class Tag(Attrs):

  def __init__(self, name, block):
    '''Initialize a `Tag` node with the given tag `name` and optional `block`.'''

    self.name = name
    self.attrs = []
    self.block = block or Block()
    self.textOnly = False

  def clone(self):
    '''Clone this tag'''

    c = Tag(self.name, self.block.clone())
    c.line = self.line
    c.attrs = self.attrs.copy()
    c.textOnly = self.textOnly

  def isInline(self):
    '''Check if this tag is an inline tag'''

    return self.name in inlineTags

  def canInline(self):
    '''Check if this tag's contents can be inlined.  Used for pretty printing.'''

    nodes = self.block.nodes

    def isInline(node):
      if node.isBlock:
        return all([isInline(n) for n in node.nodes])

      return (hasattr(node, 'isText') and node.isText) or (hasttr(node, 'isInline') and node.isInline())

    # empty tag
    if len(nodes) is 0:
      return true

    # text-only or inline-only tag
    if len(nodes) is 1:
      return isInline(nodes[0])

    # Multi-line inline-only tag
    if all([isInline(n) for n in node.nodes]):
      for i in range(1, len(nodes)):
        if(nodes[i-1].isText and nodes[i].isText):
          return False

      return True

    # mixed tag
    return False