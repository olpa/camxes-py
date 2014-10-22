
import os

from parsimonious.grammar import Grammar

from parsimonious_ext.version import PARSIMONIOUS_VERSION
from parsimonious_ext.expressions import Predicate, LookaheadPredicate

GRAMMAR_FILENAME = "camxes_ilmen.peg"

ZOI_DELIMITER_KEY = "zoi_delimiter"

def build_grammar(path, default_rule):
  if PARSIMONIOUS_VERSION > 0.5:
    return build_grammar_06(path)
  else:
    return build_grammar_05(path, default_rule)

def build_grammar_05(path, default_rule):
  f = open(path)
  grammar = Grammar(f.read(), default_rule)
  f.close()
  return grammar

def build_grammar_06(path):
  f = open(path)
  grammar = Grammar(f.read())
  f.close()
  return grammar

def _default_grammar_path():
  pwd = os.path.dirname(__file__)
  return os.path.join(pwd, GRAMMAR_FILENAME)

# Not really a predicate: Just capturing delimiter as side effect
class ZoiCaptureDelimiterPredicate(LookaheadPredicate):

  def __init__(self, member, quotation_state):
    super(ZoiCaptureDelimiterPredicate, self).__init__(member)
    self.quotation_state = quotation_state

  def evaluate(self, node):
    words = node.text.split(",")
    self.quotation_state[ZOI_DELIMITER_KEY] = words[-1]
    return True

# Is this non-space word within the quotation? (i.e. not the delimiter)
class ZoiQuotedWordPredicate(Predicate):

  def __init__(self, member, quotation_state):
    super(ZoiQuotedWordPredicate, self).__init__(member)
    self.quotation_state = quotation_state

  def evaluate(self, node):
    word = node.text.replace(",", "")
    return word != self.quotation_state[ZOI_DELIMITER_KEY]

# Is this lojban word the zoi quotation delimiter?
class ZoiDelimiterPredicate(LookaheadPredicate):

  def __init__(self, member, quotation_state):
    super(ZoiDelimiterPredicate, self).__init__(member)
    self.quotation_state = quotation_state

  def evaluate(self, node):
    words = node.text.split(",")
    return words[-1] == self.quotation_state[ZOI_DELIMITER_KEY]

class Parser:

  def __init__(self, default_rule=None, path=None):
    if not path:
      path = _default_grammar_path()
    self.grammar = build_grammar(path, default_rule)
    self._enhance_grammar(default_rule)

  def _enhance_grammar(self, default_rule):
    if (default_rule is not None) and (PARSIMONIOUS_VERSION > 0.5):
      self._apply_default_rule(default_rule)
    self._add_zoi_quotation_handling()

  def _apply_default_rule(self, rule_name):
    try:
      rule = self.grammar[rule_name]
    except KeyError:
      raise ValueError("'%s' is not a rule" % rule_name)
    self.grammar.default_rule = rule

  def _add_zoi_quotation_handling(self):
    quotation_state = {}
    self._enhance_zoi_open(quotation_state)
    self._enhance_zoi_word(quotation_state)
    self._enhance_zoi_close(quotation_state)

  def _enhance_zoi_open(self, quotation_state):
    # replace zoi_open lookahead with delimiter capturing predicate
    zoi_open = self.grammar['zoi_open']
    zoi_open_lookahead = zoi_open.members[0]
    zoi_open_word = zoi_open_lookahead.members[0]
    zoi_open_predicate = ZoiCaptureDelimiterPredicate(zoi_open_word,
                                                      quotation_state)
    zoi_open.members[0] = zoi_open_predicate

  def _enhance_zoi_word(self, quotation_state):
    # wrap zoi_word non_space_plus with quoted word predicate
    zoi_word = self.grammar['zoi_word']
    zoi_word_non_space_plus = zoi_word.members[0]
    zoi_word_predicate = ZoiQuotedWordPredicate(zoi_word_non_space_plus,
                                                quotation_state)
    zoi_word.members[0] = zoi_word_predicate

  def _enhance_zoi_close(self, quotation_state):
    # replace zoi_close lookahead with delimiter predicate
    zoi_close = self.grammar['zoi_close']
    zoi_close_lookahead = zoi_close.members[0]
    zoi_close_word = zoi_close_lookahead.members[0]
    zoi_close_predicate = ZoiDelimiterPredicate(zoi_close_word,
                                                quotation_state)
    zoi_close.members[0] = zoi_close_predicate

  def parse(self, text):
    return self.grammar.parse(text)

  def match(self, text, pos=0):
    return self.grammar.match(text, pos)

