
# pylint: disable=I0011, C0111, bare-except, too-many-ancestors

from irc.dispatcher import BaseDispatcher
from irc.factory_naming import Mixin as FactoryNamingMixin
from irc.protocol import DispatchableIrcClient

from camxes_py.structures import jbovlaste_types
from camxes_py.parsers import camxes_ilmen
from camxes_py.transformers import vlatai

class Dispatcher(BaseDispatcher, object):

    def __init__(self, client):
        super(Dispatcher, self).__init__(client)
        self.parser = camxes_ilmen.Parser('vlatai')
        self.transformer = vlatai.Transformer()

    def dispatch_command(self, nick, target, query):
        response = self._parse_vlatai(query)
        if response:
            self._msg(target, response)

    def _parse_vlatai(self, text):
        try:
            gensuha = self._transform(text)
            response = jbovlaste_types.classify(gensuha)
        except:
            response = jbovlaste_types.NALVLA
        return response

    def _transform(self, text):
        parsed = self.parser.parse(text)
        return self.transformer.transform(parsed)

    def _msg(self, target, text):
        self.client.msg(target, text)

class Protocol(FactoryNamingMixin, DispatchableIrcClient):

    def _initialize_dispatcher(self):
        self.dispatcher = Dispatcher(self)

