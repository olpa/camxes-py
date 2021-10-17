
# pylint: disable=I0011, C0111, bad-whitespace, import-error

from collections import OrderedDict
from lxml import etree

XS    = "http://www.w3.org/2001/XMLSchema"
NSMAP = { "xs" : XS }

def dumps(transformed):
    root = etree.Element("camxes", nsmap=NSMAP)
    child = _json_to_xml(transformed)
    root.append(child)
    return etree.tostring(root, pretty_print=True)

def _json_to_xml(obj):
    typ = type(obj)
    if typ == list:
        return _camxes_json_list_to_xml(obj)
    elif (typ == dict) or (obj.__class__ == OrderedDict):
        return _dict_to_xml(obj)
    elif typ == str:
        return _string_to_xml(obj)
    elif typ == int:
        return _int_to_xml(obj)
    elif hasattr(obj, "as_xml"):
        return _json_to_xml(obj.as_xml())
    else:
        raise ValueError("Can't serialize type to xml: %s" % obj.__class__)

def _camxes_json_list_to_xml(seq):
    """If first member of list is a string, treat it as symbolic"""
    head = seq[0]
    if isinstance(head, str):
        name = head
        tail = seq[1:] if len(seq) > 1 else []
        elem = etree.Element(name)
        for mem in tail:
            xml = _json_to_xml(mem)
            elem.append(xml)
    else:
        elem = _list_to_xml(seq)
    return elem

def _list_to_xml(seq):
    name = etree.QName(XS, "sequence")
    elem = etree.Element(name)
    for mem in seq:
        value = _json_to_xml(mem)
        elem.append(value)
    return elem

def _dict_to_xml(dct):
    name = etree.QName(XS, "sequence")
    elem = etree.Element(name)
    for key, val in dct.items():
        child = etree.Element(key)
        value = _json_to_xml(val)
        child.append(value)
        elem.append(child)
    return elem

def _string_to_xml(string):
    name = etree.QName(XS, "string")
    elem = etree.Element(name)
    elem.text = string
    return elem

def _int_to_xml(num):
    name = etree.QName(XS, "int")
    elem = etree.Element(name)
    elem.text = str(num)
    return elem

