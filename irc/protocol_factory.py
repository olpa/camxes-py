
from twisted.internet.protocol import ReconnectingClientFactory

class IrcClientFactory(ReconnectingClientFactory):

  def __init__(self, protocol, options):
    self.protocol = protocol
    self.nickname = options.name
    self.channels = options.channels

