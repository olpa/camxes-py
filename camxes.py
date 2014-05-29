#!/usr/bin/env python

import sys
import platform
import json

from optparse import OptionParser

import parsimonious_ext # node_types

VERSION = "v0.2"

PARSERS      = [ 'camxes-ilmen' ]
FORMATS      = [ 'camxes-json', 'debug' ]
SERIALIZERS  = [ 'json', 'json-pretty', 'json-compact' ]

IMPLEMENTATION_RECURSION_LIMIT = {
  'CPython' : 10000
}

# Texts like this one require 9700-9800 on CPython (CPython default is 1000):
#
#  mo'ini'a mo'ini'a mo'ini'a i ka'e zukte no drata be la'e di'e iseki'ubo
#  la alis za'ure'u co'a tavla i lu ju'o la dinas ba mutce le ka se claxu mi kei
#  ca le cabnicte tosa'a la dinas cu mlatu toi i a'o da ba morji tu'a le dy
#  ladru palna ca le sanmi tcika i doi dinas noi dirba mi do'u au do mi kansa
#  le cnita i u'u no smacu cu zvati le vacri i ku'i do ka'e kavbu lo volratcu
#  noi ka'u mutce le ka simsa lo'e smacu i ku'i a'u xu lo'e mlatu cu citka
#  lo'e volratcu li'u i caku la alis co'a sipydji lifri gi'e di'a senva sezysku
#  lu xu lo'e mlatu cu citka lo'e volratcu i xu lo'e mlatu cu citka lo'e
#  volratcu li'u esu'oroibo lu xu lo'e volratcu cu citka lo'e mlatu li'u
#  iseja'ebo na vajni mutce fa le du'u porsi makau ki'u le nu abu ka'e spuda no
#  le re preti i abu lifri le nu pu'o sipna kei gi'e puzi co'a senva le nu abu
#  xanjaisi'u cadzu kansa la dinas gi'e cusku lu ju'i doi dinas ko mi jungau
#  le jetnu i xu do su'oroi citka lo volratcu li'u ca le nu suksa fa le nu abu
#  le cpana be lo derxi be loi grana ku joi loi sudga pezli mo'u farlu
#
# Pypy doesn't need to increase limit; untested on Jython and IronPython

def check_parser_option(option, opt_str, value, parser):
  if value in PARSERS:
    setattr(parser.values, option.dest, value)
  else:
    bad_parser()

def bad_parser():
  raise ValueError("Value for parser must be one of: %s" % \
    (", ".join(PARSERS)))

def check_format_option(option, opt_str, value, parser):
  if value in FORMATS:
    setattr(parser.values, option.dest, value)
  else:
    bad_format()

def bad_format():
  raise ValueError("Value for format must be one of: %s" % \
    (", ".join(FORMATS)))

def check_serializer_option(option, opt_str, value, parser):
  if value in SERIALIZERS:
    setattr(parser.values, option.dest, value)
  else:
    bad_serializer()

def bad_serializer():
  raise ValueError("Value for serializer must be one of: %s" % \
    (", ".join(SERIALIZERS)))

def configure_platform():
  impl = python_platform()
  if impl in IMPLEMENTATION_RECURSION_LIMIT:
    stack_limit = IMPLEMENTATION_RECURSION_LIMIT[impl]
    sys.setrecursionlimit(stack_limit)

def python_platform():
  if python_version() >= 260:
    return platform.python_implementation()
  else:
    # NOTE: Untested with Java < 2.7; IronPython < 2.6 is not detected
    return "Jython" if platform.system() == "Java" else "CPython"

def python_version():
  (major, minor, patch) = platform.python_version_tuple()
  return (major * 10) + minor

def main(text, options):
  parser_option = options.parser if len(PARSERS) > 1 else "camxes-ilmen"
  parsed = parse(text, parser_option)
  tranformed = transform(parsed, options.formatter)
  print serialize(tranformed, options.serializer)

def parse(text, parser):
  if parser == 'camxes-ilmen':
    from parsers import camxes_ilmen
    return camxes_ilmen.Parser().parse(text)
  else:
    bad_parser()

def transform(parsed, transformer):
  if transformer == 'camxes-json':
    from transformers import camxes_json
    return camxes_json.Transformer().transform(parsed)
  elif transformer == 'debug':
    from transformers import debug
    return debug.Transformer().transform(parsed)
  else:
    bad_transformer()

def serialize(transformed, fmt):
  if fmt == 'json':
    return json.dumps(transformed)
  elif fmt == 'json-compact': # a.k.a. JSON.stringify()
    return json.dumps(transformed, separators=(',', ':'))
  elif fmt == 'json-pretty':
    return json.dumps(transformed, indent=4)
  else:
    bad_serializer()

if __name__ == '__main__':

  usage_fmt = "usage: %prog [ options ] { input }"
  options = OptionParser(usage=usage_fmt, version="%prog " + VERSION)

  if len(PARSERS) > 1:
    options.add_option("-p", "--parser",
                       help=("options: %s" % (", ".join(PARSERS))) + \
                         " [default: %default]",
                       type="string", action="callback",
                       dest="parser", default="camxes-ilmen",
                       callback=check_parser_option)

  options.add_option("-f", "--formatter",
                     help=("options: %s" % (", ".join(FORMATS))) + \
                       " [default: %default]",
                     type="string", action="callback",
                     dest="formatter", default="camxes-json",
                     callback=check_format_option)

  options.add_option("-s", "--serializer",
                     help=("options: %s" % (", ".join(SERIALIZERS))) + \
                       " [default: %default]",
                     type="string", action="callback",
                     dest="serializer", default="json-compact",
                     callback=check_serializer_option)

  (params, argv) = options.parse_args()
  text = " ".join(argv)

  configure_platform()
  main(text, params)

