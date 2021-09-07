#!/usr/bin/env python3

# pylint: disable=I0011,C0111

import sys

from parsimonious.exceptions import ParseError

from camxes_py.structures import jbovlaste_types
from camxes import configure_platform
from camxes_py.parsers.camxes_ilmen import Parser
from camxes_py.transformers.vlatai import Visitor

VLATAI_RULE = "vlatai"

def run(text):
    parser = build_parser()
    gensuha = analyze_morphology(parser, text)
    print(jbovlaste_types.classify(gensuha))

def build_parser():
    return Parser(VLATAI_RULE)

def analyze_morphology(parser, text):
    visitor = Visitor()
    gensuha = None
    try:
        parsed = parser.parse(text)
        gensuha = visitor.visit(parsed)
    except ParseError:
        pass
    return gensuha

def _main():
    configure_platform()
    text = " ".join(sys.argv[1:])
    run(text)

if __name__ == '__main__':
    _main()
