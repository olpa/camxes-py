
# pylint: disable=I0011, C0111, C0326, too-many-arguments, protected-access

"""
Decorates parsimonious node and expression classes to record the type of
expression used to parse each node.
"""

from parsimonious.nodes import Node
from parsimonious.expressions import Literal, Regex, Sequence, OneOf, \
                                     Lookahead, Not, Optional,        \
                                     ZeroOrMore, OneOrMore

from .util import add_to_class, with_original, renamed

LITERAL     = "LITERAL"
REGEX       = "REGEX"
SEQUENCE    = "SEQUENCE"
ALTERNATION = "ALTERNATION"
LOOKAHEAD   = "LOOKAHEAD"
NOT         = "NOT"
OPTIONAL    = "OPTIONAL"
STAR        = "STAR"
PLUS        = "PLUS"

Literal.NODE_TYPE    = LITERAL
Regex.NODE_TYPE      = REGEX
Sequence.NODE_TYPE   = SEQUENCE
OneOf.NODE_TYPE      = ALTERNATION
Lookahead.NODE_TYPE  = LOOKAHEAD
Not.NODE_TYPE        = NOT
Optional.NODE_TYPE   = OPTIONAL
ZeroOrMore.NODE_TYPE = STAR
OneOrMore.NODE_TYPE  = PLUS

# Node extensions

@add_to_class(Node)
@renamed('description')
def node_description(self):
    return self.expr._as_rhs() if self.expr else None

@add_to_class(Node)
def node_type(self):
    return self.expr.NODE_TYPE if self.expr else None

