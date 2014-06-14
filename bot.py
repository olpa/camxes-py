
import sys

from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.python import log

from camxes import VERSION
from irc.protocol_factory import IrcClientFactory
from irc.vlatai import Protocol

DEFAULT_HOST     = "irc.freenode.net"
DEFAULT_PORT     = 6667
DEFAULT_CHANNELS = [ "#lojban" ]
DEFAULT_NICKNAME = "vlatai"

def main(options):
  factory = IrcClientFactory(Protocol, options)
  log.startLogging(sys.stdout)
  reactor.connectTCP(options.host, options.port, factory)
  reactor.run()

if __name__ == '__main__':

  args = ArgumentParser()

  args.add_argument("-H", "--host",
                    dest="host", default=DEFAULT_HOST)

  args.add_argument("-p", "--port",
                    dest="port", default=DEFAULT_PORT)

  args.add_argument("-c", "--channels",
                    action="append",
                    dest="channels", default=[])

  args.add_argument("-n", "--name",
                    dest="name", default=DEFAULT_NICKNAME)

  args.add_argument("-v", "--version",
                    action="version", version=VERSION)

  options = args.parse_args()
  if len(options.channels) == 0:
    options.channels = DEFAULT_CHANNELS
  main(options)

