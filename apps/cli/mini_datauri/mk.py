#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_datauri (tab-separated ops):
  p <uri>      parse a data: URI  -> "mt|hex|repr", or "ERR <message>"
  d <text>     discover data: URIs in a string -> "<count>" then space-joined
               "mt|hex" items (mt is "-" when the media type is empty/None)
The output columns use '|' between media type and payload and a space between
discovered items; neither byte is in the data-URI character set, so they are
unambiguous. mk.py writes only literal inputs (no library import); oracle.py
replays every job against the vendored datauri library. See README.md."""
import os
os.makedirs("data", exist_ok=True)

# parse jobs: the happy paths, both encodings, the None-media-type and empty
# payload cases, the three error branches, and a payload over 20 bytes so the
# repr truncation (data[:17] + b'...') is exercised.
parse_uris = [
    "data:,plain",
    "data:text/plain,hello%20world",
    "data:text/plain;charset=utf-8,Hello%2C%20World%21",
    "data:text/html;base64,PGgxPkhpITwvaDE+",
    "data:image/gif;base64,R0lGODlhAQABAAAAACwAAAAAAQABAAA=",
    "data:application/octet-stream;base64,3q2+7w==",
    "data:;base64,SGVsbG8h",
    "data:text/plain,",
    "data:text/plain,a+b",
    "data:text/plain,100%25done",
    "data:text/plain,%E2%9C%93",
    "data:text/plain,%zznope",
    "data:application/json,%7B%22k%22%3A1%7D",
    "data:text/plain;base64,QQ==",
    "data:text/plain;base64,QUJD",
    "data:text/css,body%7Bcolor%3Ared%7D",
    "nope",
    "data:",
    "data:text/plain",
    "data:text/plain;base64,A",
    "data:text/plain,this is a longer payload exceeding twenty bytes for repr",
    "data:text/plain;base64,VGhpcyBpcyBhIGZhaXJseSBsb25nIGJhc2U2NCBwYXlsb2Fk",
]

discover_docs = [
    "see data:text/plain,hi and data:text/html;base64,PGgxPg== end",
    "no uris here at all",
    "data:,x data:text/plain;base64,QUJD junk data: notacompletething",
    "prefix data:application/json,%7B%22k%22%3A1%7D suffix",
    "two in a row data:,a data:,b done",
    "a bad base64 data:x;base64,A then a good one data:,ok",
]

lines = []
for u in parse_uris:
    lines.append("p\t%s" % u)
for d in discover_docs:
    lines.append("d\t%s" % d)

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
