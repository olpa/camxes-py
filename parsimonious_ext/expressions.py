
from parsimonious.expressions import _Compound
from parsimonious.nodes import Node

# Note: these predicates do not consult the cache

LOOKAHEAD_PREDICATE = "LOOKAHEAD_PREDICATE"

class Predicate(_Compound):

  def _match(self, text, pos, cache, error):
    node = self.members[0]._match(text, pos, cache, error)
    if node is not None and self.evaluate(node):
      return node
    else:
      return None

  def evaluate(self, node):
      return True

  def _as_rhs(self):
    return u'&%s{}' % self._unicode_members()[0]

class LookaheadPredicate(_Compound):

  def _match(self, text, pos, cache, error):
    node = self.members[0]._match(text, pos, cache, error)
    if node is not None and self.evaluate(node):
      out = Node(self.name, text, pos, pos) # like lookahead
      out.node_type = LOOKAHEAD_PREDICATE
      return out
    else:
      return None

