from . node import Node

class Block(Node):
  '''Block inherits from Node'''
  is_block = True

  def __init__(self, node = None):
    '''Initializes a Block'''
    self._nodes = [];
    self._yield = False
    if node != None:
      self.append(node)

  def push(self, node):
    '''Pushes the `node` to the top of this block's stack'''
    return self._nodes.append(node)

  def is_empty(self):
    '''Returns `True` if this block is empty'''
    return len(self._nodes) == 0

  def unshift(self, node):
    '''Inserts `node` in to the beginning of the block and returns the length'''
    self._nodes.insert(0, node)
    return len(self._nodes)

  def include_block(self):
    '''Return the "last" block, or the first `yield` node'''
    ret = self

    for node in self._nodes:
      if node._yield:
        return node
      elif node.textOnly:
        continue
      elif hasattr(node, 'include_block'):
        ret = node.include_block()
      elif hasattr(node, 'block') and node.block.is_empty():
        ret = node.block.include_block()

      if ret._yield:
        return ret

    return ret

  def clone(self):
    '''Clones this block'''

    newBlock = Block()
    for node in self._nodes:
      newBlock.append(node.clone())

    return newBlock

  @property
  def nodes(self):
    return self._nodes

  @nodes.setter
  def nodes(self, value):
    self._nodes = value

  @property
  def yield_(self):
      return self._yield_

  @yield_.setter
  def yield_(self, value):
      self._yield_ = value

