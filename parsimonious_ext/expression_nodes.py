
# pylint: disable=I0011, C0111, C0326, too-many-arguments, protected-access

"""
Decorates parsimonious node and expression classes to record the type of
expression used to parse each node.
"""

from functools import partial, wraps

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

def add_to_class(cls):
    """Add method, replacing any previous method by name"""
    def decorator(decorated):
        setattr(cls, decorated.__name__, decorated)
        return decorated
    return decorator

def with_original(original_function):
    if hasattr(original_function, '__func__'): # unwrap python 2 unbound methods
        original_function = original_function.__func__
    def decorator(decorated):
        decorated = partial(decorated, original=original_function)
        @wraps(original_function)
        def decoration(self, *args, **kwargs):
            return decorated(self, *args, **kwargs)
        return decoration
    return decorator

def renamed(new_name):
    def decorator(decorated):
        decorated.__name__ = new_name
        return decorated
    return decorator

# Node extensions

@add_to_class(Node)
@with_original(Node.__init__)
def node_init(self, expr, full_text, start, end,
              children=None, original=None):
    original(self, expr, full_text, start, end, children)
    self.expression = None

@add_to_class(Node)
@renamed('description')
def node_description(self):
    return self.expression._as_rhs() if self.expression else None

@add_to_class(Node)
def node_type(self):
    return self.expression.NODE_TYPE if self.expression else None

# Literal extensions

@add_to_class(Literal)
@with_original(Literal._uncached_match)
def literal_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

def expression_node(node, expression):
    if node is not None:
        node.expression = expression
    return node

# Regex extensions

@add_to_class(Regex)
@with_original(Regex._uncached_match)
def regex_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

# Sequence extensions

@add_to_class(Sequence)
@with_original(Sequence._uncached_match)
def sequence_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(Sequence)
@with_original(Sequence._as_rhs)
def sequence_grouped_as_rhs(self, original=None):
    return u'(%s)' % original(self)

# OneOf extensions

@add_to_class(OneOf)
@with_original(OneOf._uncached_match)
def one_of_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(OneOf)
@with_original(OneOf._as_rhs)
def one_of_grouped_as_rhs(self, original=None):
    return u'(%s)' % original(self)

# Lookahead extensions

@add_to_class(Lookahead)
@with_original(Lookahead._uncached_match)
def lookahead_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(Lookahead)
@wraps(Lookahead._as_rhs)
def lookahead_grouped_as_rhs(self):
    fmt = u'&(%s)' if len(self.members) > 1 else u'&%s'
    return fmt % self._unicode_members()[0]

# Not extensions

@add_to_class(Not)
@with_original(Not._uncached_match)
def not_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(Not)
@wraps(Not._as_rhs)
def not_grouped_as_rhs(self):
    fmt = u'!(%s)' if len(self.members) > 1 else u'!%s'
    return fmt % self._unicode_members()[0]

# Optional extensions

@add_to_class(Optional)
@with_original(Optional._uncached_match)
def optional_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(Optional)
@wraps(Optional._as_rhs)
def optional_grouped_as_rhs(self):
    fmt = u'(%s)?' if len(self.members) > 1 else u'%s?'
    return fmt % self._unicode_members()[0]

# ZeroOrMore extensions

@add_to_class(ZeroOrMore)
@with_original(ZeroOrMore._uncached_match)
def zero_or_more_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(ZeroOrMore)
@wraps(ZeroOrMore._as_rhs)
def zero_or_more_grouped_as_rhs(self):
    fmt = u'(%s)*' if len(self.members) > 1 else u'%s*'
    return fmt % self._unicode_members()[0]

# OneOrMore extensions

@add_to_class(OneOrMore)
@with_original(OneOrMore._uncached_match)
def one_or_more_uncached_match(self, text, pos, cache, error, original=None):
    node = original(self, text, pos, cache, error)
    return expression_node(node, self)

@add_to_class(OneOrMore)
@wraps(OneOrMore._as_rhs)
def one_or_more_grouped_as_rhs(self):
    fmt = u'(%s)+' if len(self.members) > 1 else u'%s+'
    return fmt % self._unicode_members()[0]

