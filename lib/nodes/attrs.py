from . node import Node

class Attrs(Node):

  def __init__(self):
    self.attrs = []

  def setAttribute(self, name, val, escaped):
    """
    Set attribute `name` to `val`, keep in mind these become
    part of a raw js object literal, so to quote a value you must
    '"quote me"', otherwise or example 'user.name' is literal JavaScript.
    """
    self.attrs.append({'name':name, 'val':val, 'escaped':escaped});
    return self

  def removeAttribute(self, name):
    attrs = [a for a in self.attrs if a['name'] != name]

  def getAttribute(self, name):
    for a in self.attrs:
      if a['name'] == name:
        return a

    return None
