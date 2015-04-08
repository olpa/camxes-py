
# pylint: disable=I0011, C0111, too-few-public-methods, no-self-use

from collections import OrderedDict

from parsimonious.nodes import NodeVisitor

KEY_ORDER = {
    "name"                : 1,
    "type"                : 2,
    "description" : 3,
    "text"                : 4,
    "pos"                 : 5,
    "children"        : 6
}

def _sorted_node_dictionary(dct):
    return OrderedDict(sorted(dct.items(), key=lambda t: KEY_ORDER[t[0]]))

def generic_node(node, visited_children):

    node_dictionary = {"type" : node.node_type()}

    if node.expr_name:
        node_dictionary["name"] = node.expr_name
    else:
        node_dictionary["description"] = node.description()

    start = node_dictionary["pos"] = node.start

    length = node.end - start
    if length > 0 and node.text:
        node_dictionary["text"] = node.text

    if visited_children:
        node_dictionary["children"] = visited_children

    return _sorted_node_dictionary(node_dictionary)

class Transformer(object):

    def transform(self, parsed):
        return Visitor().visit(parsed)

class Visitor(NodeVisitor):

    def generic_visit(self, node, visited_children):
        return generic_node(node, visited_children)

