#!/usr/bin/env python3

# pylint: disable=I0011, C0111, C0326

import os
import json

from collections import OrderedDict

from parsimonious.exceptions import ParseError

from camxes import __version__, configure_platform
from camxes_py.parsers import camxes_ilmen
from camxes_py.transformers import camxes_json, camxes_morphology

ENV = OrderedDict([
    ("engine", "camxes-py"),
    ("version", __version__),
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
    with open(path) as input_file:
        input_json = json.load(input_file)
    return input_json

def process_input(input_json):
    input_specs = input_json["specs"]
    parser = camxes_ilmen.Parser()
    json_transformer = camxes_json.Transformer()
    morph_transformer = camxes_morphology.Transformer()
    return [
        process_spec(spec, parser, json_transformer, morph_transformer) \
            for spec in input_specs
    ]

def process_spec(input_spec, parser, json_transformer, morph_transformer):
    output_spec = OrderedDict()
    output_spec["md5"] = input_spec["md5"]
    text = output_spec["txt"] = input_spec["txt"]

    out = morph = None
    try:
        print("text: " + text)
        parsed = parser.parse(text)
        out = transform_to_serial(parsed, json_transformer)
        morph = transform_to_serial(parsed, morph_transformer)
    except ParseError:
        out = "ERROR"
        morph = None
    if out != input_spec["out"]:
        print_error(text, input_spec["out"], out)

    output_spec["out"] = out
    if morph:
        output_spec["morph"] = morph

    return output_spec

def transform_to_serial(parsed, transformer):
    default_serializer = default_object_serializer(transformer)
    transformed = transformer.transform(parsed)
    return json.dumps(transformed,
                      separators=(',', ':'),
                      default=default_serializer)

def default_object_serializer(transformer):
    if hasattr(transformer, 'default_serializer'):
        return transformer.default_serializer()
    else:
        return lambda x: x.__dict__

def print_error(text, was, now):
    print("----------------")
    print(text)
    print("WAS: %s" % was)
    print("IS:  %s" % now)

def dump_results(specs, output_path):
    with open(output_path, 'w') as output_file:
        results = OrderedDict([
            ("env", ENV),
            ("specs", specs)
        ])
        json.dump(results, output_file, indent=4)

if __name__ == '__main__':
    configure_platform()
    main()
