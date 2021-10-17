
# pylint: disable=I0011, C0111, no-self-use, invalid-name

from collections.abc import Iterable

def flatten(nested):
    return list(flatten_inner(nested))

def flatten_inner(nested):
    for el in nested:
        if isinstance(el, (str, bytes)):
            yield el
        else:
            try:
                yield from flatten(iter(el))
            except TypeError:
                yield el
