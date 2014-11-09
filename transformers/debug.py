
import re

from parsimonious.nodes import NodeVisitor

from parsimonious_ext.expression_nodes import LITERAL, REGEX
from camxes_morphology import is_selmaho_expression

def _is_consonant(name):
  return re.match(r"^[bcdfghjklmnpqrstvxz]$", name)

def _is_vowel(name):
  return re.match(r"^[aeiouy]$", name)

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

  def default_serializer(self):
    return lambda x : x.as_json()

class Visitor(NodeVisitor):

  def generic_visit(self, node, visited_children):
    if node.expr_name:
      return self._visit_named_node(node, visited_children)
    else:
      return ExpressionNode(node, visited_children)

  def _visit_named_node(self, node, visited_children):
    if _is_consonant(node.expr_name) or _is_vowel(node.expr_name):
      return TextValueNode(node, visited_children)
    elif is_selmaho_expression(node.expr_name):
      return TextContainerNode(node, visited_children)
    else:
      return ExpressionNode(node, visited_children)

  def visit_dot_star(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_CMEVLA(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_CMAVO(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_zoi_word(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_lujvo(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_fuhivla(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_gismu(self, node, visited_children):
    return TextContainerNode(node, visited_children)

  def visit_spaces(self, node, visited_children):
    return TextContainerNode(node, visited_children)

class DebugNode:

  def __init__(self, node, children):
    self.node = node
    self.children = children

  def label(self):
    expr_name = self.name()
    return expr_name if expr_name else self.description()

  def name(self):
    return self.node.expr_name

  def description(self):
    return self.node.description()

  def node_type(self):
    return self.node.node_type()

  def text(self):
    return self.node.text

  def is_empty(self):
    text = self.text()
    return (not text) or (text == "")

  def as_json(self):
    return self.as_json_container()

  def as_xml(self):
    name = (self.name() or self.node_type())
    xml_json = [ name ]
    for child_node in self.children:
      child_xml_json = child_node.as_xml()
      xml_json.append(child_xml_json)
    return xml_json

  def as_json_container(self):
    children = [ c for c in self.children if not c.is_empty() ]
    return { self.label() : children }

  def as_text_container(self):
    return { self.label() : self.text() }

class ExpressionNode(DebugNode):

  def as_json(self):
    node_type = self.node_type()
    if node_type in (LITERAL, REGEX):
      return self.text()
    else:
      return self.as_json_container()

  def as_xml(self):
    node_type = self.node_type()
    if node_type in (LITERAL, REGEX):
      return self.text()
    else:
      return DebugNode.as_xml(self)

class TextContainerNode(DebugNode):

  def as_json(self):
    return self.as_text_container()

  def as_xml(self):
    name = (self.name() or self.node_type())
    return [ name, self.text() ]

class TextValueNode(DebugNode):

  def as_json(self):
    return self.text()

  def as_xml(self):
    return self.text()

