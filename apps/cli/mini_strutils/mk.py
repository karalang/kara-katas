#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_strutils, one job per line (tab-separated):

    c2u  \t <s>                    camel2under
    u2c  \t <s>                    under2camel
    ord  \t <numstr>               ordinalize
    a10  \t <s>                    a10n (numeronym)
    slug \t <s>                    slugify (delim '_')
    pil  \t <range_string>         parse_int_list
    fil  \t <space-separated ints> format_int_list
    cil  \t <range_string> \t <start> \t <end|*>   complement_int_list
    irl  \t <range_string>         int_ranges_from_int_list
    hrl  \t <item>|<item>|...      human_readable_list

Inputs use only the argument field(s); the first field is the op, so a value may
itself contain commas, dashes or spaces. `*` in a cil `end` field means the
Python default (None). The cases walk the boundaries each function branches on:
camel/underscore transitions and acronym runs, the ordinal teens, range
compaction and its de-dup / repeat / reversed-bound paths, and the 0/1/2/3-item
human-readable list.
"""
import os

C2U = ["BasicParseTest", "complexTokenizer", "HTTPResponse", "parse2HTML",
       "A", "aB", "snake_case", "x", "getHTTPResponseCode", "IOError",
       "simpleXML", "HTML5Parser", "already_under", ""]
U2C = ["complex_tokenizer", "basic_parse_test", "__foo", "a_b_c", "x", "_",
       "hello", "foo__bar", "", "UPPER_CASE", "trailing_"]
ORD = ["0", "1", "2", "3", "4", "5", "11", "12", "13", "21", "22", "23",
       "100", "101", "111", "1515", "3694839230", "hi", ""]
A10 = ["abbreviation", "internationalization", "localization", "",
       "a", "ab", "abc", "accessibility", "kubernetes"]
SLUG = ["First post! Hi!!!!~1    ", "Hello, World", "  ...  ",
        "MixOf_Things-and.more", "", "already_clean", "CAPS LOCK",
        "a::b//c  d", "punct!@#$only"]
PIL = ["1,3,5-8,10-11,15", "1", "", "1,1,2,2", "8-5", "10,9,8", "100-100",
       "1,2,3,4,5", "5", "3-3"]
FIL = ["1 3 5 6 7 8 10 11 15", "1", "", "1 2 3", "5 5 5 6", "1 2 4 5 6 8",
       "10 9 8 7", "42", "1 2 3 100 101 102"]
# (range_string, start, end-as-string with * = None)
CIL = [("1,3,5-8,10-11,15", "0", "*"), ("1,3,5-8,10-11,15", "1", "*"),
       ("1,3,5-8,10-11,15", "0", "15"), ("1,3,5-8,10-11,15", "0", "14"),
       ("1,3,5-8,10-11,15", "0", "20"), ("1,3,5-8,10-11,15", "0", "0"),
       ("1,3,5-8", "2", "3"), ("1,3,5-8", "1", "1"), ("", "0", "*"),
       ("1,3,5-8", "20", "10")]
IRL = ["1,3,5-8,10-11,15", "1", "", "2-2", "1,2,3", "5-9"]
HRL = ["a", "a|b", "a|b|c", "one|two|three|four", "", "apple|banana",
       "red|green|blue|yellow|purple"]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for s in C2U:
        fh.write("c2u\t%s\n" % s)
    for s in U2C:
        fh.write("u2c\t%s\n" % s)
    for s in ORD:
        fh.write("ord\t%s\n" % s)
    for s in A10:
        fh.write("a10\t%s\n" % s)
    for s in SLUG:
        fh.write("slug\t%s\n" % s)
    for s in PIL:
        fh.write("pil\t%s\n" % s)
    for s in FIL:
        fh.write("fil\t%s\n" % s)
    for (rs, st, en) in CIL:
        fh.write("cil\t%s\t%s\t%s\n" % (rs, st, en))
    for s in IRL:
        fh.write("irl\t%s\n" % s)
    for s in HRL:
        fh.write("hrl\t%s\n" % s)
