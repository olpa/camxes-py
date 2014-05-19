
import os

from parsimonious.grammar import Grammar

GRAMMAR_FILENAME = "camxes.peg"

def read_grammar(path):
  f = open(path)
  grammar = Grammar(f.read())
  f.close()
  return grammar

def _default_grammar_path():
  pwd = os.path.dirname(__file__)
  return os.path.join(pwd, GRAMMAR_FILENAME)

class Parser:

  def __init__(self, path=None):
    if not path:
      path = _default_grammar_path()
    self.grammar = read_grammar(path)

  def parse(self, text):
    return self.grammar.parse(text)

