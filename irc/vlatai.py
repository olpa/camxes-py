
from twisted.python import log

import dispatcher
import factory_naming

from structures import jbovlaste_types
from parsers import camxes_ilmen
from transformers import vlatai
from protocol import DispatchableIrcClient

from structures.gensuha import Cmavo

class Dispatcher(dispatcher.BaseDispatcher):

  def __init__(self, client):
    self.client = client
    self.parser = camxes_ilmen.Parser('vlatai')
    self.transformer = vlatai.Transformer()

  def dispatch_command(self, nick, target, query):
    response = self._parse_vlatai(query, nick)
    if response:
      self._msg(target, response)

  def _parse_vlatai(self, text, nick):
    try:
      gensuha = self._transform(text)
      response = jbovlaste_types.classify(gensuha)
    except Exception, e:
      response = jbovlaste_types.NALVLA
    return response

  def _transform(self, text):
    parsed = self.parser.parse(text)
    return self.transformer.transform(parsed)

  def _msg(self, target, text):
    self.client.msg(target, text)

class Protocol(factory_naming.Mixin, DispatchableIrcClient):

  def _initialize_dispatcher(self):
    self.dispatcher = Dispatcher(self)

