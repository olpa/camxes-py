
from collections import OrderedDict

from parsimonious.nodes import NodeVisitor

KEY_ORDER = {
  "name"        : 1,
  "type"        : 2,
  "description" : 3,
  "text"        : 4,
  "pos"         : 5,
  "children"    : 6
}

def _sorted_node_dictionary(d):
  return OrderedDict(sorted(d.items(), key=lambda t: KEY_ORDER[t[0]]))

def generic_node(node, visited_children):

  n = { "type" : node.node_type() }

  if node.expr_name:
    n["name"] = node.expr_name
  else:
    n["description"] = node.description()

  start = n["pos"] = node.start

  l = node.end - start
  if l > 0 and node.text:
    n["text"] = node.text

  if visited_children:
    n["children"] = visited_children

  return _sorted_node_dictionary(n)

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

class Visitor(NodeVisitor):

  def generic_visit(self, node, visited_children):
    return generic_node(node, visited_children)

