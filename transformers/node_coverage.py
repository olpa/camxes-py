
from parsimonious.nodes import NodeVisitor

class Transformer:

  def __init__(self, parser):
    self.visitor = Visitor([ expr for expr in parser.grammar ])

  def transform(self, parsed):
    self.visit(parsed)
    return self.visits()

  def visit(self, parsed):
    self.visitor.visit(parsed)

  def visits(self):
    visited = self.visitor.visited
    visits = [] # sort by visits desc, expr_name asc
    sorted_exprs = [ expr for expr in sorted(visited) ]
    for expr in sorted(sorted_exprs, key=visited.get, reverse=True):
      visits.append([ expr, visited[expr] ])
    return visits

class Visitor(NodeVisitor):

  def __init__(self, expressions):
    self.visited = self._initialize_visit_count(expressions)

  def _initialize_visit_count(self, expressions):
    visited = {}
    for expr in expressions:
      visited[expr] = 0
    return visited

  def generic_visit(self, node, visited_children):
    name = node.expr_name
    if name:
      self.visited[name] += 1
    return None

