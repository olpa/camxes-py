
from parsimonious.nodes import Node
from parsimonious.expressions \
    import Literal, Regex, Sequence, OneOf, Lookahead, Not, Optional, ZeroOrMore, OneOrMore

LITERAL     = "LITERAL"
REGEX       = "REGEX"
SEQUENCE    = "SEQUENCE"
ALTERNATION = "ALTERNATION"
LOOKAHEAD   = "LOOKAHEAD"
NOT         = "NOT"
OPTIONAL    = "OPTIONAL"
STAR        = "STAR"
PLUS        = "PLUS"

##

Node._orig_init = Node.__init__
def _expression_node_init(self, expr_name, full_text, start, end, children=None):
  Node._orig_init(self, expr_name, full_text, start, end, children)
  self.expression = None
Node.__init__ = _expression_node_init

def _node_description(self):
  return self.expression._as_rhs() if self.expression else None
Node.description = _node_description

def _node_type(self):
  return self.expression.NODE_TYPE if self.expression else None
Node.node_type = _node_type

##

def expression_node(node, expression):
  if node is not None:
    node.expression = expression
  return node

#

Literal.NODE_TYPE = LITERAL

Literal._orig_uncached_match = Literal._uncached_match
def _literal_uncached_match(self, text, pos, cache, error):
  node = Literal._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
Literal._uncached_match = _literal_uncached_match

#

Regex.NODE_TYPE = REGEX

Regex._orig_uncached_match = Regex._uncached_match
def _regex_uncached_match(self, text, pos, cache, error):
  node = Regex._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
Regex._uncached_match = _regex_uncached_match

#

Sequence.NODE_TYPE = SEQUENCE

Sequence._orig_uncached_match = Sequence._uncached_match
def _sequence_uncached_match(self, text, pos, cache, error):
  node = Sequence._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
Sequence._uncached_match = _sequence_uncached_match

Sequence._orig_as_rhs = Sequence._as_rhs
def _sequence_grouped_as_rhs(self):
  return u'(%s)' % self._orig_as_rhs()
Sequence._as_rhs = _sequence_grouped_as_rhs

#

OneOf.NODE_TYPE = ALTERNATION

OneOf._orig_uncached_match = OneOf._uncached_match
def _alternation_uncached_match(self, text, pos, cache, error):
  node = OneOf._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
OneOf._uncached_match = _alternation_uncached_match

OneOf._orig_as_rhs = OneOf._as_rhs
def _alternation_grouped_as_rhs(self):
  return u'(%s)' % self._orig_as_rhs()
OneOf._as_rhs = _alternation_grouped_as_rhs

#

Lookahead.NODE_TYPE = LOOKAHEAD

Lookahead._orig_uncached_match = Lookahead._uncached_match
def _lookahead_uncached_match(self, text, pos, cache, error):
  node = Lookahead._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
Lookahead._uncached_match = _lookahead_uncached_match

def _lookahead_grouped_as_rhs(self):
  fmt = u'&(%s)' if len(self.members) > 1 else u'&%s'
  return fmt % self._unicode_members()[0]
Lookahead._as_rhs = _lookahead_grouped_as_rhs

#

Not.NODE_TYPE = NOT

Not._orig_uncached_match = Not._uncached_match
def _not_uncached_match(self, text, pos, cache, error):
  node = Not._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
Not._uncached_match = _not_uncached_match

def _not_grouped_as_rhs(self):
  fmt = u'!(%s)' if len(self.members) > 1 else u'!%s'
  return fmt % self._unicode_members()[0]
Not._as_rhs = _not_grouped_as_rhs

#

Optional.NODE_TYPE = OPTIONAL

Optional._orig_uncached_match = Optional._uncached_match
def _optional_uncached_match(self, text, pos, cache, error):
  node = Optional._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
Optional._uncached_match = _optional_uncached_match

def _optional_grouped_as_rhs(self):
  fmt = u'(%s)?' if len(self.members) > 1 else u'%s?'
  return fmt % self._unicode_members()[0]
Optional._as_rhs = _optional_grouped_as_rhs

#

ZeroOrMore.NODE_TYPE = STAR

ZeroOrMore._orig_uncached_match = ZeroOrMore._uncached_match
def _star_uncached_match(self, text, pos, cache, error):
  node = ZeroOrMore._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
ZeroOrMore._uncached_match = _star_uncached_match

def _star_grouped_as_rhs(self):
  fmt = u'(%s)*' if len(self.members) > 1 else u'%s*'
  return fmt % self._unicode_members()[0]
ZeroOrMore._as_rhs = _star_grouped_as_rhs

#

OneOrMore.NODE_TYPE = PLUS
OneOrMore._orig_uncached_match = OneOrMore._uncached_match
def _plus_uncached_match(self, text, pos, cache, error):
  node = OneOrMore._orig_uncached_match(self, text, pos, cache, error)
  return expression_node(node, self)
OneOrMore._uncached_match = _plus_uncached_match

def _plus_grouped_as_rhs(self):
  fmt = u'(%s)+' if len(self.members) > 1 else u'%s+'
  return fmt % self._unicode_members()[0]
OneOrMore._as_rhs = _plus_grouped_as_rhs

