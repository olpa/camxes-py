
# pylint: disable=I0011, C0111, bare-except, no-self-use, too-many-ancestors

import json

from irc.dispatcher import BaseDispatcher
from irc.factory_naming import Mixin as FactoryNamingMixin
from irc.protocol import DispatchableIrcClient
from parsers.camxes_ilmen import Parser
from transformers.camxes_morphology import Transformer

ERROR_MESSAGE = ".u'u mi na pu genturfa'i"

class Dispatcher(BaseDispatcher):

    def __init__(self, client):
        super(Dispatcher, self).__init__(client)
        self.parser = Parser('morphology')
        self.transformer = Transformer()

    def dispatch_command(self, nick, target, query):
        response = self._parse_morphology(query, nick)
        if response:
            self._msg(target, response)

    def _parse_morphology(self, text, _): # nick ignored
        try:
            transformed = self._transform(text)
            response = self._serialize(transformed)
        except:
            response = self._error_response()
        return response

    def _transform(self, text):
        parsed = self.parser.parse(text)
        return self.transformer.transform(parsed)

    def _serialize(self, transformed):
        default_serializer = self.transformer.default_serializer()
        return json.dumps(transformed, default=default_serializer)

    def _error_response(self):
        return ERROR_MESSAGE

    def _msg(self, target, text):
        self.client.msg(target, text)

class Protocol(DispatchableIrcClient, FactoryNamingMixin):

    def _initialize_dispatcher(self):
        self.dispatcher = Dispatcher(self)

