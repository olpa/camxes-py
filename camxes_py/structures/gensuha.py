
# pylint: disable=I0011, C0111, too-few-public-methods, bad-whitespace

from collections import OrderedDict

# Glossary

# genturfa'i : parser ("grammar-structure discoverer")

# terge'a : grammatical-text

# A text which is accepted by a {genturfa'i} is a {terge'a}, a grammatical
# text according to the {gerna} of the {genturfa'i}.

# genturtai : grammar-structure form

class Gensuha(object):
    """
    gensu'a: grammar structure

    A structure discovered by the parser, with complex {gensu'a}
    being composed of less complex {gensu'a}.

    Parsed {gensu'a} may be classified by form of composition, {genturtai}.
    Individual characters, {lerfu}, are atomic {gensu'a}. A sequence of {lerfu}
    compose a {lerpoi}. Lojban's rules of morphology define specific {lerpoi}
    forms, such as {cmevla}, {brivla} and {cmavo}. Different forms of {brivla}
    are distinguished as {gismu}, {lujvo} and {fu'ivla}. A sequence of {brivla}
    compose a {tanru}.
    """

    GENTURTAI = "naltarmi"

    def lerpoi(self):
        raise NotImplementedError

    def __str__(self):
        return ''.join(self.lerpoi)

class Lerpoi(Gensuha):
    """
    lerpoi: letteral sequence

    A string of characters.
    """

    GENTURTAI = "lerpoi"

    def __init__(self, lerpoi):
        self.lerpoi = lerpoi

    def as_json(self):
        return OrderedDict([
            ( "genturtai", self.GENTURTAI ),
            ( "lerpoi",    self.lerpoi    )
        ])

    def as_xml(self):
        return self.as_json()

class Naljbo(Lerpoi):

    GENTURTAI = "naljbo"

class Valsi(Lerpoi):

    GENTURTAI = "valsi"

class Cmevla(Valsi):

    GENTURTAI = "cmevla"

class Selbri(object): # not itself a structure, but a property of some structures
    pass

class Brivla(Valsi, Selbri):
    pass

class Gismu(Brivla):

    GENTURTAI = "gismu"

class Jvodunlei(object): # not a structure
    pass

class Lujvo(Brivla, Jvodunlei):

    GENTURTAI = "lujvo"

class Fuhivla(Brivla):

    GENTURTAI = "fuhivla"

class Cmavo(Valsi):

    GENTURTAI = "cmavo"

    def __init__(self, lerpoi, selmaho):
        super(Cmavo, self).__init__(lerpoi)
        self.selmaho = selmaho

    def as_json(self):
        return OrderedDict([
            ( "genturtai", self.GENTURTAI ),
            ( "selmaho",   self.selmaho   ),
            ( "lerpoi",    self.lerpoi    )
        ])

class Vlapoi(Gensuha):
    """
    vlapoi: word sequence
    """

    GENTURTAI = "vlapoi"

    def __init__(self, vlapoi):
        self.vlapoi = vlapoi

    @property
    def lerpoi(self):
        return [lerfu for valsi in self.vlapoi for lerfu in valsi.lerpoi]

    def as_json(self):
        return OrderedDict([
            ( "genturtai", self.GENTURTAI ),
            ( "vlapoi",    self.vlapoi    )
        ])

class ZeiLujvo(Vlapoi, Jvodunlei):

    GENTURTAI = "zei-lujvo"

class Lerdunlei(object): # not a structure
    pass

class BuLetteral(Vlapoi, Lerdunlei):

    GENTURTAI = "bu-letteral"

class Tosmabru(Vlapoi):

    GENTURTAI = "tosmabru"

class Slinkuhi(Vlapoi):

    GENTURTAI = "slinku'i"

