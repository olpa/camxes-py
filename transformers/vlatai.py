
from compiler.ast import flatten

from transformers import camxes_morphology
from structures.gensuha import BuLetteral, ZeiLujvo

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

  def default_serializer(self):
    return lambda x : x.as_json()

class Visitor(camxes_morphology.Visitor):

  def visit_vlatai(self, node, visited_children):
    return visited_children[1]

  def visit_vlatai_bu_clause(self, node, visited_children):
    return BuLetteral(flatten(visited_children))

  def visit_vlatai_zei_clause(self, node, visited_children):
    return ZeiLujvo(flatten(visited_children))

