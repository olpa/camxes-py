
from parsimonious.nodes import Node
from parsimonious.expressions import Literal, Regex, Sequence, OneOf, Lookahead, Not, Optional, ZeroOrMore, OneOrMore

LITERAL     = "LITERAL"
REGEX       = "REGEX"
SEQUENCE    = "SEQUENCE"
ALTERNATION = "ALTERNATION"
LOOKAHEAD   = "LOOKAHEAD"
NOT         = "NOT"
OPTIONAL    = "OPTIONAL"
STAR        = "STAR"
PLUS        = "PLUS"

def typed_node(node, typ):
  if node is not None:
    node.node_type = typ
  return node

# Decorate Node initializer and Expression _uncached_match to ensure that
# Node instances always have a node_type, and Node instances returned by
# Expression instance uncached matching are assigned a node_type according
# to the type of the expression that generated them.

Node._orig_init = Node.__init__
def _typed_node_init(self, expr_name, full_text, start, end, children=None):
  Node._orig_init(self, expr_name, full_text, start, end, children)
  self.node_type = None
Node.__init__ = _typed_node_init

Literal._orig_uncached_match = Literal._uncached_match
def _literal_uncached_match(self, text, pos, cache, error):
  node = Literal._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, LITERAL)
Literal._uncached_match = _literal_uncached_match

Regex._orig_uncached_match = Regex._uncached_match
def _regex_uncached_match(self, text, pos, cache, error):
  node = Regex._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, REGEX)
Regex._uncached_match = _regex_uncached_match

Sequence._orig_uncached_match = Sequence._uncached_match
def _sequence_uncached_match(self, text, pos, cache, error):
  node = Sequence._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, SEQUENCE)
Sequence._uncached_match = _sequence_uncached_match

OneOf._orig_uncached_match = OneOf._uncached_match
def _alternation_uncached_match(self, text, pos, cache, error):
  node = OneOf._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, ALTERNATION)
OneOf._uncached_match = _alternation_uncached_match

Lookahead._orig_uncached_match = Lookahead._uncached_match
def _lookahead_uncached_match(self, text, pos, cache, error):
  node = Lookahead._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, LOOKAHEAD)
Lookahead._uncached_match = _lookahead_uncached_match

Not._orig_uncached_match = Not._uncached_match
def _not_uncached_match(self, text, pos, cache, error):
  node = Not._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, NOT)
Not._uncached_match = _not_uncached_match

Optional._orig_uncached_match = Optional._uncached_match
def _optional_uncached_match(self, text, pos, cache, error):
  node = Optional._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, OPTIONAL)
Optional._uncached_match = _optional_uncached_match

ZeroOrMore._orig_uncached_match = ZeroOrMore._uncached_match
def _star_uncached_match(self, text, pos, cache, error):
  node = ZeroOrMore._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, STAR)
ZeroOrMore._uncached_match = _star_uncached_match

OneOrMore._orig_uncached_match = OneOrMore._uncached_match
def _plus_uncached_match(self, text, pos, cache, error):
  node = OneOrMore._orig_uncached_match(self, text, pos, cache, error)
  return typed_node(node, PLUS)
OneOrMore._uncached_match = _plus_uncached_match

