
from collections import OrderedDict
from lxml import etree

XS    = "http://www.w3.org/2001/XMLSchema"
NSMAP = { "xs" : XS }

def dumps(transformed):
  root = etree.Element("camxes", nsmap=NSMAP)
  child = _json_to_xml(transformed)
  root.append(child)
  return etree.tostring(root, pretty_print=True)

def _json_to_xml(x):
  typ = type(x)
  if typ == list:
    return _camxes_json_list_to_xml(x)
  elif (typ == dict) or (x.__class__ == OrderedDict):
    return _dict_to_xml(x)
  elif typ in (str, unicode):
    return _string_to_xml(x)
  elif typ == int:
    return _int_to_xml(x)
  elif hasattr(x, "as_xml"):
    return _json_to_xml(x.as_xml())
  else:
    raise ValueError("Can't serialize type to xml: %s" % x.__class__)

def _camxes_json_list_to_xml(x):
  """If first member of list is a string, treat it as symbolic"""
  head = x[0]
  if type(head) != str:
    el = _list_to_xml(x)
  else:
    name = head
    tail = x[1:] if len(x) > 1 else []
    el = etree.Element(name)
    for c in tail:
      e = _json_to_xml(c)
      el.append(e)
  return el

def _list_to_xml(x):
  name = etree.QName(XS, "sequence")
  el = etree.Element(name)
  for i in x:
    value = _json_to_xml(i)
    el.append(value)
  return el

def _dict_to_xml(x):
  name = etree.QName(XS, "sequence")
  el = etree.Element(name)
  for k, v in x.iteritems():
    child = etree.Element(k)
    value = _json_to_xml(v)
    child.append(value)
    el.append(child)
  return el

def _string_to_xml(x):
  name = etree.QName(XS, "string")
  el = etree.Element(name)
  el.text = x
  return el

def _int_to_xml(x):
  name = etree.QName(XS, "int")
  el = etree.Element(name)
  el.text = str(x)
  return el

