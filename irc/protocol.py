
from twisted.python import log
from twisted.words.protocols.irc import IRCClient

from dispatcher import BaseDispatcher

class DispatchableIrcClient(IRCClient):

  def signedOn(self):
    log.msg('* Logged on')
    self._initialize_dispatcher()
    self._notify_factory_signed_on()
    self._join_channels()

  def _initialize_dispatcher(self):
    """Template method for initializing a dispatcher."""
    if not hasattr(self, 'dispatcher'):
      log.msg("default dispatcher")
      self.dispatcher = BaseDispatcher(self)

  def _notify_factory_signed_on(self):
    if hasattr(self.factory, 'resetDelay'): # e.g. ReconnectingClientFactory
      self.factory.resetDelay()

  def _join_channels(self):
    log.msg("joining channel: %s" % self.factory.channels)
    for channel in self.factory.channels:
      log.msg("join channel: %s" % channel)
      self.join(channel)

  # log NOTICE but do not automate reply per RFC
  def noticed(self, user, channel, message):
    log.msg('<%(nickname)s> %(message)s' %
            dict(nickname=self.nickname, message=message))
    pass # prevent delegation to privmsg

  def privmsg(self, user, receive_channel, message):
    user_nickname = user[:user.index('!')]
    if receive_channel == self.nickname: # i.e. private message
      self._dispatch_private_message(user_nickname, user_nickname, message)
    else:
      self._dispatch_public_message(user_nickname, receive_channel, message)

  def _dispatch_private_message(self, nick, response_channel, message):
    self.dispatcher.dispatch_private_message(nick, response_channel, message)

  def _dispatch_public_message(self, nick, response_channel, message):
    self.dispatcher.dispatch_public_message(nick, response_channel, message)

  def msg(self, response_channel, message):
    """Log messages sent by the client"""
    log.msg('<%(nickname)s> %(message)s' %
            dict(nickname=self.nickname, message=message))
    IRCClient.msg(self, response_channel, message)

