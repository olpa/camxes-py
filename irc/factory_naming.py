
class Mixin:

  """Mixin for IRC protocols with factories that provide a nick"""

  def _get_nickname(self):
    return self.factory.nickname
  nickname = property(_get_nickname)

