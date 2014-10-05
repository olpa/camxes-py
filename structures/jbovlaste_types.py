
from structures.gensuha \
  import Cmevla, Gismu, Lujvo, Fuhivla, Cmavo, ZeiLujvo, BuLetteral, Tosmabru, Slinkuhi

# legacy classifications
CMEVLA        = "cmevla"
GISMU         = "gismu"
LUJVO         = "lujvo"
FUHIVLA       = "fu'ivla"
CMAVO         = "cmavo"
NALVLA        = "nalvla"

# new classifications
CMAVO_COMPOUND = "cmavo-compound"
BU_LETTERAL    = "bu-letteral"
ZEI_LUJVO      = "zei-lujvo"

# non-jvs types
TOSMABRU       = "valrtosmabru"
SLINKUHI       = "valslinku'i"

def classify(gensuha):
  if gensuha is None or len(gensuha) < 1:
    return NALVLA
  elif len(gensuha) == 1:
    return classify_gensuha(gensuha[0])
  else:
    return classify_gensuha_sequence(gensuha)

def classify_gensuha(gensuha):
  if isinstance(gensuha, Cmevla):
    return CMEVLA
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
  elif isinstance(gensuha, Tosmabru):
    return TOSMABRU
  elif isinstance(gensuha, Slinkuhi):
    return SLINKUHI
  else:
    return NALVLA

def classify_gensuha_sequence(gensuha):
  if is_cmavo_sequence(gensuha):
    return CMAVO_COMPOUND
  else:
    return NALVLA

def is_cmavo_sequence(gensuha):
  return all(map(lambda g : isinstance(g, Cmavo), gensuha))

