
# pylint: disable=I0011, C0111, C0326, too-many-arguments, protected-access

from functools import partial

from parsimonious.nodes import Node
from parsimonious.expressions import Literal, Regex, Sequence, OneOf, \
                                     Lookahead, Not, Optional,        \
                                     ZeroOrMore, OneOrMore

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

def wrap_method(cls, func_name):
    def decorator(func):
        wrapped = getattr(cls, func_name)
        unbound_wrapper = partial(func, original=wrapped)
        def wrapper(self, *args, **kwargs):
            return unbound_wrapper(self, *args, **kwargs)
        setattr(cls, func_name, wrapper)
        return wrapper
    return decorator

def patch(cls, func_name):
    """Add method, replacing any previous method by name"""
    def decorator(func):
        setattr(cls, func_name, func)
        return func
    return decorator

# Node extensions

@wrap_method(Node, '__init__')
def node_init(self, expr, full_text, start, end,
              children=None, original=None):
    original(self, expr, full_text, start, end, children)
    self.expression = None

@patch(Node, 'description')
def node_description(self):
    return self.expression._as_rhs() if self.expression else None

@patch(Node, 'node_type')
def node_type(self):
    return self.expression.NODE_TYPE if self.expression else None

# Literal extensions

@wrap_method(Literal, '_uncached_match')
def literal_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

def expression_node(node, expression):
    if node is not None:
        node.expression = expression
    return node

# Regex extensions

@wrap_method(Regex, '_uncached_match')
def regex_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

# Sequence extensions

@wrap_method(Sequence, '_uncached_match')
def sequence_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@wrap_method(Sequence, '_as_rhs')
def sequence_grouped_as_rhs(self, original=None):
    return u'(%s)' % original(self)

# OneOf extensions

@wrap_method(OneOf, '_uncached_match')
def one_of_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@wrap_method(OneOf, '_as_rhs')
def one_of_grouped_as_rhs(self, original=None):
    return u'(%s)' % original(self)

# Lookahead extensions

@wrap_method(Lookahead, '_uncached_match')
def lookahead_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@patch(Lookahead, '_as_rhs')
def lookahead_grouped_as_rhs(self):
    fmt = u'&(%s)' if len(self.members) > 1 else u'&%s'
    return fmt % self._unicode_members()[0]

# Not extensions

@wrap_method(Not, '_uncached_match')
def not_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@patch(Not, '_as_rhs')
def not_grouped_as_rhs(self):
    fmt = u'!(%s)' if len(self.members) > 1 else u'!%s'
    return fmt % self._unicode_members()[0]

# Optional extensions

@wrap_method(Optional, '_uncached_match')
def optional_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@patch(Optional, '_as_rhs')
def optional_grouped_as_rhs(self):
    fmt = u'(%s)?' if len(self.members) > 1 else u'%s?'
    return fmt % self._unicode_members()[0]

# ZeroOrMore extensions

@wrap_method(ZeroOrMore, '_uncached_match')
def zero_or_more_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@patch(ZeroOrMore, '_as_rhs')
def zero_or_more_grouped_as_rhs(self):
    fmt = u'(%s)*' if len(self.members) > 1 else u'%s*'
    return fmt % self._unicode_members()[0]

# OneOrMore extensions

@wrap_method(OneOrMore, '_uncached_match')
def one_or_more_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@patch(OneOrMore, '_as_rhs')
def one_or_more_grouped_as_rhs(self):
    fmt = u'(%s)+' if len(self.members) > 1 else u'%s+'
    return fmt % self._unicode_members()[0]

