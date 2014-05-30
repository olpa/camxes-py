
camxes-py is a pure python implementation of the lojban "camxes" PEG parser,
originally implemented by Robin Lee Powell and Jorge Llambías using Java
Rats! and ported to JavaScript by Masato Hagiwara, with additional improvements
by Ilmen.

USAGE
=====

To generate a transformed parse tree:

  python camxes.py "coi munje"

OPTIONS
=======

The --formattter (-f) option controls the transformation of the parse tree.
Supported options include: debug, node-coverage and camxes-json (default)

The --serializer (-s) option controls the serialization of the
transformed parse tree. Supported options include: json, json-pretty,
and json-compact (default)

DEPENDENCIES
============

camxes-py depends on the "parsimonious" PEG parser library.

TESTING
=======

camxes-py is tested with the corpus of more than 22K test sentences
that Robin Lee Powell originally assembled to test the first (Java Rats!)
camxes implementation.

These sentences have been converted to UTF-8, indexed by MD5/base64 token.
deduplicated and packaged in "sentences.json" in the "test" directory.
Each sentence is marked "GOOD" or "BAD" if it was so-commented in the
original source file. Other sentences are marked "UNKNOWN".

Running "test.py" will parse all of the test sentences, comparing the results
to the output of ilmentufa camxes.js (cached in "camxes_ilmen_js.json")
and regenerating "camxes_ilmen_py.json".

LICENSE
=======

The scripts and modules in this implementation may be copied, modified,
and distributed under the terms of the accompanied license, "LICENSE.txt".

