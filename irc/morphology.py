
import json

import dispatcher
import factory_naming

from parsers import camxes_ilmen
from transformers import camxes_morphology
from protocol import DispatchableIrcClient

ERROR_MESSAGE = ".u'u mi na pu genturfa'i"

class Dispatcher(dispatcher.BaseDispatcher):

  def __init__(self, client):
    self.client = client
    self.parser = camxes_ilmen.Parser()
    self.transformer = camxes_morphology.Transformer()

  def dispatch_command(self, nick, target, query):
    response = self._parse_morphology(query, nick)
    if response:
      self._msg(target, response)

  def _parse_morphology(self, text, nick):
    try:
      transformed = self._transform(text)
      response = self._serialize(transformed)
    except Exception, e:
      response = self._error_response(text, e)
    return response

  def _transform(self, text):
    parsed = self.parser.parse(text)
    return self.transformer.transform(parsed)

  def _serialize(self, transformed):
    default_serializer = self.transformer.default_serializer()
    return json.dumps(transformed, default = default_serializer)

  def _error_response(self, text, e):
    return ERROR_MESSAGE

  def _msg(self, target, text):
    self.client.msg(target, text)

# NOTE: factory_naming.Mixin must be first
class Protocol(factory_naming.Mixin, DispatchableIrcClient):

  def _initialize_dispatcher(self):
    self.dispatcher = Dispatcher(self)

