#!/usr/bin/env python3
"""Writes data/jobs.tsv: one URL to normalize per line, tab-separated.

op is always `norm`; arg is the URL. Inputs are ASCII (so NFC normalization
and IDNA host encoding are no-ops, and the port stays pure integer/string),
and every URL carries an http/https/ftp authority — the scheme-with-authority
shape url_normalize's defaults target.
"""
import os

URLS = [
    # scheme and host case, trailing dot, empty-path -> "/"
    "http://example.com",
    "http://Example.COM/",
    "HTTP://example.com/A?Z=1&z=2",
    "http://example.com.",
    # default-port removal, non-default kept
    "http://example.com:80/path",
    "https://example.com:443/",
    "http://example.com:8080/a",
    "ftp://example.com:21/f",
    # dot-segment collapsing
    "http://example.com/a/./b/../c",
    "http://example.com/a/../../b",
    # percent-encoding normalization (case, unreserved decode, essential encode)
    "http://example.com/%7euser/",
    "http://example.com/a b",
    "http://example.com/a%2fb",
    "http://example.com/%e2%9c%93",
    # query sorting, utm stripping, trailing &? cleanup
    "http://example.com/?b=2&a=1",
    "http://example.com/?utm_source=news&x=1",
    "http://example.com?x=1&",
    # shebang -> escaped fragment
    "http://example.com/page#!key=val",
    # userinfo handling
    "http://user:pass@example.com/",
    "http://@example.com/",
    # fragment quoting
    "http://example.com/p?q=a+b#frag ment",
    # scheme / authority supplied for bare and protocol-relative inputs
    "example.com/path",
    "//example.com/x",
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w") as fh:
    for u in URLS:
        fh.write("norm\t" + u + "\n")
