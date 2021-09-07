from .parsers import camxes_ilmen
from .transformers import camxes_json


def parse(text, parser=None, rule=None, transformer=None):
    if parser is None:
        parser = camxes_ilmen.Parser(rule)
    if transformer is None:
        transformer = camxes_json.Transformer()
    parsed = parser.parse(text)
    transformed = transformer.transform(parsed)
    return transformed
