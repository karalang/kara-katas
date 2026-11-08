# Not NLTK's own __init__.py, which imports the whole toolkit: an empty
# package, so that `nltk.stem.lancaster` (vendored verbatim from NLTK 3.10.4)
# can be imported on its own.
