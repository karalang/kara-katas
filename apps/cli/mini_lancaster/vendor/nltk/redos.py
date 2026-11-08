# Not NLTK's own nltk/redos.py, which runs every pattern through the
# third-party `regex` engine under a timeout. The Lancaster stemmer's two
# patterns are linear, so the stdlib's compile stands in for it here.
from re import compile  # noqa: F401
