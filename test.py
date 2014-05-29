
import os
import json

from collections import OrderedDict

from parsimonious.exceptions import ParseError

from camxes import VERSION, configure_platform
from parsers import camxes_ilmen
from transformers import camxes_json

ENV = OrderedDict([
  ("engine", "camxes-py"),
  ("version", VERSION),
  ("format", "camxes-json"),
  ("serialization", "json-compact")
])

TEST_DIRECTORY  = "test"
INPUT_FILENAME  = "camxes_ilmen_js.json"
OUTPUT_FILENAME = "camxes_ilmen_py.json"

PWD = os.path.dirname(__file__)
INPUT_PATH = os.path.join(PWD, TEST_DIRECTORY, INPUT_FILENAME)
OUTPUT_PATH = os.path.join(PWD, TEST_DIRECTORY, OUTPUT_FILENAME)

def main():
  input_json = read_json(INPUT_PATH)
  specs = process_input(input_json)
  dump_results(specs, OUTPUT_PATH)

def read_json(path):
  input_file = open(path)
  input_json = json.load(input_file)
  input_file.close()
  return input_json

def process_input(input_json):
  input_specs = input_json["specs"]
  parser = camxes_ilmen.Parser()
  transformer = camxes_json.Transformer()
  return [ process_spec(spec, parser, transformer) for spec in input_specs ]

def process_spec(input_spec, parser, transformer):
  output_spec = OrderedDict()
  output_spec["md5"] = input_spec["md5"]
  text = output_spec["txt"] = input_spec["txt"]

  out = None
  try:
    out = process_text(text, parser, transformer)
  except ParseError as e:
    out = "ERROR"
  if out != input_spec["out"]:
    print_error(text, input_spec["out"], out)

  output_spec["out"] = out
  return output_spec

def process_text(text, parser, transformer):
  parsed = parser.parse(text)
  transformed = transformer.transform(parsed)
  return json.dumps(transformed, separators=(',', ':'))

def print_error(text, was, now):
  print "----------------"
  print text
  print "WAS: %s" % was
  print "IS:  %s" % now

def dump_results(specs, output_path):
  output_file = open(output_path, 'w')
  results = OrderedDict([
    ("env", ENV),
    ("specs", specs)
  ])
  json.dump(results, output_file, indent=4)
  output_file.close()

if __name__ == '__main__':
  configure_platform()
  main()
