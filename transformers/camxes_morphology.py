
import re

from collections import OrderedDict
from compiler.ast import flatten

from parsimonious.nodes import NodeVisitor

from parsimonious_ext.node_types import LITERAL, REGEX

# Glossary
#
# genturfa'i : parser ("grammar-structure discoverer")
# gensu'a    : grammar-structure
# genturtai  : grammar-structure form
#              (e.g. cmevla, gismu, lujvo, fuhivla, cmavo
# terge'a    : grammatical-text
# tergentai  : grammatical-text form
#              (e.g. valsi, jufra)
# lerpoi     : character sequence

class Gensuha:

  GENTURTAI = "naltarmi"

  def __init__(self, lerpoi):
    self.lerpoi = lerpoi

  def as_json(self):
    return OrderedDict([
      ( "genturtai", self.GENTURTAI ),
      ( "lerpoi",    self.lerpoi    )
    ])

class Cmavo(Gensuha):

  GENTURTAI = "cmavo"

  def __init__(self, lerpoi, selmaho):
    self.lerpoi = lerpoi
    self.selmaho = selmaho

  def as_json(self):
    return OrderedDict([
      ( "genturtai", self.GENTURTAI ),
      ( "selmaho",   self.selmaho   ),
      ( "lerpoi",    self.lerpoi    )
    ])

class Cmevla(Gensuha):

  GENTURTAI = "cmevla"

class Brivla(Gensuha):
  pass

class Gismu(Brivla):

  GENTURTAI = "gismu"

class Lujvo(Brivla):

  GENTURTAI = "lujvo"

class Fuhivla(Brivla):

  GENTURTAI = "fuhivla"

class Naljbo(Gensuha):

  GENTURTAI = "naljbo"

# flatten and join textual nodes
def lerpoi(children):
  return "".join(flatten(children))

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

  def default_serializer(self):
    return lambda x : x.as_json()

class Visitor(NodeVisitor):

  def visit_space_char(self, node, visited_children):
    return []

  def visit_EOF(self, node, visited_children):
    return []

  def visit_CMEVLA(self, node, visited_children):
    return Cmevla(lerpoi(visited_children))

  def visit_BRIVLA(self, node, visited_children):
    return flatten(visited_children)

  def visit_gismu_2(self, node, visited_children):
    return Gismu(lerpoi(visited_children))

  def visit_lujvo(self, node, visited_children):
    return Lujvo(lerpoi(visited_children))

  def visit_fuhivla(self, node, visited_children):
    return Fuhivla(lerpoi(visited_children))

  # handle by selmaho in generic_visit()
  def visit_CMAVO(self, node, visited_children):
    return flatten(visited_children)

  def visit_BY(self, node, visited_children):
    children = flatten(visited_children)
    if isinstance(children[0], Gensuha):
      value = children # ybu = Y + BU
    else:
      value = Cmavo("".join(children), node.expr_name)
    return value

  def visit_zoi_word(self, node, visited_children):
    return Naljbo(lerpoi(visited_children))

  def visit_non_lojban_word(self, node, visited_children):
    return Naljbo(lerpoi(visited_children))

  def generic_visit(self, node, visited_children):

    # CMAVO by selmaho
    if node.expr_name and re.match(r"[A-Z]+(h[AEIOU])?$", node.expr_name):
      value = Cmavo(lerpoi(visited_children), node.expr_name)

    elif node.node_type == LITERAL:
      value = node.text

    elif node.node_type == REGEX:
      value = node.text

    else:
      value = flatten(visited_children)

    return value

