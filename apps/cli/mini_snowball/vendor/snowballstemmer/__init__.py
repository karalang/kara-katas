"""Minimal package init vendored for mini_snowball: exposes only the Porter
stemmer path (the single algorithm this app ports). The upstream __init__
eagerly imports all 38 language stemmers; only the three Porter files
(among.py, basestemmer.py, porter_stemmer.py) are vendored here, unmodified,
so the oracle runs exactly the code the Kara port mirrors. Upstream is
snowballstemmer 3.1.1 (BSD-3-Clause); see LICENSE-snowballstemmer.txt."""
from .porter_stemmer import PorterStemmer

__all__ = ("stemmer",)

_languages = {"porter": PorterStemmer, "english_porter": PorterStemmer}


def stemmer(language):
    key = language.lower()
    if key in _languages:
        return _languages[key]()
    raise KeyError("mini_snowball vendors only the 'porter' algorithm")
