#!/usr/bin/env python

import sys
import json

from optparse import OptionParser

import debug

from parser import Parser

sys.setrecursionlimit(1700) # System default is 1000
# Texts like this one require 1600-1700:
# i lu cumki fa le nu fy batci sei la alis noi nasai xankydji le nu troci le nu cipra cu spuda li'u

VERSION = "v0.1"

TRANFORMERS = [ 'debug' ]

FORMATS = [ 'json', 'json-pretty', 'json-compact' ]

def check_transformer_option(option, opt_str, value, parser):
    if value in TRANFORMERS:
      setattr(parser.values, option.dest, value)
    else:
      bad_transformer()

def bad_transformer():
  raise ValueError("Value for transformer must be one of: %s" % \
    (", ".join(TRANFORMERS)))

def check_format_option(option, opt_str, value, parser):
    if value in FORMATS:
      setattr(parser.values, option.dest, value)
    else:
      bad_format()

def bad_format():
  raise ValueError("Value for format must be one of: %s" % \
    (", ".join(FORMATS)))

def parse(text):
  return Parser().parse(text)

def transform(parsed, tree):
  if tree == 'debug':
    return debug.Visitor().visit(parsed)
  else:
    bad_transformer()

def serialize(tree, fmt):
  if fmt == 'json':
    return json.dumps(tree)
  elif fmt == 'json-compact': # JSON.stringify()
    return json.dumps(tree, separators=(',', ':'))
  elif fmt == 'json-pretty':
    return json.dumps(tree, indent=4)
  else:
    bad_format()

def main(text, options):
  tree = parse(text)
  tranformed = transform(tree, options.transformer)
  print serialize(tranformed, options.fmt)

if __name__ == '__main__':

  usage_fmt = "usage: %prog [ options ] { input }"
  options = OptionParser(usage=usage_fmt, version="%prog " + VERSION)

  options.add_option("-t", "--transformer",
                     help=("options: %s" % (", ".join(TRANFORMERS))) + \
                       " [default: %default]",
                     type="string", action="callback",
                     dest="transformer", default="debug",
                     callback=check_transformer_option)

  options.add_option("-f", "--format",
                     help=("options: %s" % (", ".join(FORMATS))) + \
                       " [default: %default]",
                     type="string", action="callback",
                     dest="fmt", default="json-compact",
                     callback=check_format_option)

  (params, argv) = options.parse_args()
  text = " ".join(argv)
  main(text, params)

