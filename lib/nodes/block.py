from . node import Node

class Block(Node):
  """Block inherits from Node"""
  isBlock = True

  def __init__(self, node):
    """Initializes a Block"""
    self.nodes = [];
    self.yield_ = False
    if node != None:
      self.append(node)

  def push(self, node):
    """Pushes the `node` to the top of this block's stack"""
    return self.nodes.append(node)

  def isEmpty(self):
    """Returns `True` if this block is empty"""
    return len(self.nodes) == 0

  def unshift(self, node):
    """Inserts `node` in to the beginning of the block and returns the length"""
    self.nodes.insert(0, node)
    return len(self.nodes)

  def includeBlock(self):
    """Return the "last" block, or the first `yield` node"""
    ret = self

    for node in nodes:
      if node.yield_:
        return node
      elif node.textOnly:
        continue
      elif hasattr(node, 'includeBlock'):
        ret = node.includeBlock()
      elif hasattr(node, 'block') and node.block.isEmpty():
        ret = node.block.includeBlock()

      if ret.yield_:
        return ret

    return ret

  def clone(self):
    """Clones this block"""

    newBlock = Block()
    for node in nodes:
      newBlock.append(node.clone())

    return newBlock