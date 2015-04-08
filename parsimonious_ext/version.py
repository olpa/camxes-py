
# pylint: disable=I0011, C0111, unused-import

try:
    from parsimonious.expressions import Compound
    PARSIMONIOUS_VERSION = 0.6
except ImportError:
    PARSIMONIOUS_VERSION = 0.5

