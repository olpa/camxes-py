
import sys

from parsimonious.exceptions import ParseError

from camxes import configure_platform
from parsers.camxes_ilmen import Parser
from transformers.vlatai import Visitor
from structures.gensuha \
  import Cmevla, Gismu, Lujvo, Fuhivla, Cmavo, ZeiLujvo, BuLetteral

VLATAI_RULE = "vlatai"

# legacy vlatai classifications
CMENE         = "cmene"
GISMU         = "gismu"
LUJVO         = "lujvo"
FUHIVLA       = "fu'ivla"
CMAVO         = "cmavo"
NALVLA        = "nalvla"

# new classifications
CMAVO_COMPOUND = "cmavo-compound"
BU_LETTERAL    = "bu-letteral"
ZEI_LUJVO      = "zei-lujvo"

def main(text):
  gensuha = analyze_morphology(text)
  print classify(gensuha)

def analyze_morphology(text):
  parser = Parser(VLATAI_RULE)
  visitor = Visitor()

  gensuha = None
  try:
    parsed = parser.parse(text)
    gensuha = visitor.visit(parsed)
  except ParseError as e:
    pass
  return gensuha

def classify(gensuha):
  if gensuha is None or len(gensuha) < 1:
    return NALVLA
  elif len(gensuha) == 1:
    return classify_gensuha(gensuha[0])
  else:
    return classify_gensuha_sequence(gensuha)

def classify_gensuha(gensuha):
  if isinstance(gensuha, Cmevla):
    return CMENE
  elif isinstance(gensuha, Gismu):
    return GISMU
  elif isinstance(gensuha, Lujvo):
    return LUJVO
  elif isinstance(gensuha, Fuhivla):
    return FUHIVLA
  elif isinstance(gensuha, Cmavo):
    return CMAVO
  elif isinstance(gensuha, ZeiLujvo):
    return ZEI_LUJVO
  elif isinstance(gensuha, BuLetteral):
    return BU_LETTERAL
  else:
    return NALVLA

def classify_gensuha_sequence(gensuha):
  if is_cmavo_sequence(gensuha):
    return CMAVO_COMPOUND
  else:
    return NALVLA

def is_cmavo_sequence(gensuha):
  return all(map(lambda g : isinstance(g, Cmavo), gensuha))

if __name__ == '__main__':

  text = " ".join(sys.argv[1:])

  configure_platform()
  main(text)

