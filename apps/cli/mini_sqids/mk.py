#!/usr/bin/env python3
"""Writes data/jobs.tsv and data/blocklist.txt. A job line is tab-separated:

    new <alphabet|-> <min_length> <blocklist|->   build a Sqids (- = default)
    enc <n,n,...>                                 encode with the current one
    dec <id>                                      decode with the current one

A custom blocklist is comma-separated (an empty field is an empty blocklist).
data/blocklist.txt is the library's DEFAULT_BLOCKLIST, one word per line,
read as a literal out of vendor/sqids/constants.py (the module is not
imported). Run: python3 -s -P -B mk.py"""
import ast
import os

DEF = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

JOBS = [
    # the default Sqids
    ("new", "-", "0", "-"),
    ("enc", "1,2,3"),
    ("dec", "86Rf07"),
    ("enc", "0"),
    ("enc", "1"),
    ("enc", "0,0,0,0,0"),
    ("enc", "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20"),
    ("enc", "9223372036854775807"),
    ("enc", "9223372036854775807,0,9223372036854775807"),
    ("dec", "AqkYhRmbHpEX"),
    ("dec", "CuaMqvAPlJnDSJr9lqFQvLPnBC"),
    ("enc", "1000000,2000000"),
    ("enc", "100,200,300"),
    ("enc", "4572721"),
    ("dec", "aho1e"),
    ("dec", "JExTR"),
    ("enc", ""),
    ("dec", ""),
    ("dec", "*"),
    ("dec", "86Rf0-7"),
    ("enc", "-1"),
    ("enc", "1,-5,2"),
    # min_length padding
    ("new", "-", "6", "-"),
    ("enc", "1,2,3"),
    ("new", "-", "10", "-"),
    ("enc", "1,2,3"),
    ("enc", "0"),
    ("dec", "86Rf07xd4z"),
    ("new", "-", "62", "-"),
    ("enc", "1,2,3"),
    ("enc", "0"),
    ("new", "-", "100", "-"),
    ("enc", "7"),
    ("new", "-", "255", "-"),
    ("enc", "42"),
    # custom alphabets, default blocklist filtered against them
    ("new", "0123456789abcdef", "0", "-"),
    ("enc", "1,2,3"),
    ("enc", "255,4096,65535"),
    ("new", "abc", "0", "-"),
    ("enc", "1,2,3"),
    ("enc", "100"),
    ("new", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0", "-"),
    ("enc", "1,2,3"),
    ("new", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0", "sxnzkl"),
    ("enc", "1,2,3"),
    ("dec", "IBSHOZ"),
    ("new", "abcdefghijklmnopqrstuvwxyz", "8", "-"),
    ("enc", "31,41,59,26,53"),
    # custom blocklists
    ("new", "-", "0", ""),
    ("enc", "4572721"),
    ("enc", "0"),
    ("new", "-", "0", "ArUO"),
    ("enc", "4572721"),
    ("dec", "ArUO"),
    ("enc", "100000"),
    ("dec", "QyG4"),
    ("new", "-", "0", "JSwXFaosAN,OCjV9JK64o,rBHf,79SM,7tE6"),
    ("enc", "1000000,2000000"),
    ("dec", "1aYeB7bRUt"),
    ("new", "-", "0", "86Rf07,se8ojk,ARsz1p,Q8AI49,5sQRZO"),
    ("dec", "86Rf07"),
    ("dec", "se8ojk"),
    ("dec", "ARsz1p"),
    ("enc", "1,2,3"),
    ("new", "-", "0", "pnd"),
    ("enc", "1000"),
    ("new", "-", "0", "bM,ab,x"),
    ("enc", "0"),
    ("new", "abc", "0", "ab!,abc!,xyz"),
    ("enc", "5"),
    # the re-generation limit
    ("new", "abc", "3", "cab,abc,bca"),
    ("enc", "0"),
    # constructor errors
    ("new", "ab", "0", "-"),
    ("new", "aabcdef", "0", "-"),
    ("new", "abcdéfg", "0", "-"),
    ("new", "-", "256", "-"),
    ("new", "-", "-1", "-"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for job in JOBS:
        fh.write("\t".join(job) + "\n")

src = open("vendor/sqids/constants.py", encoding="utf-8").read()
start = src.index("DEFAULT_BLOCKLIST = [") + len("DEFAULT_BLOCKLIST = ")
end = src.index("]", start) + 1
words = ast.literal_eval(src[start:end])
with open("data/blocklist.txt", "w", encoding="utf-8") as fh:
    for w in words:
        fh.write(w + "\n")
print("wrote %d jobs, %d blocklist words" % (len(JOBS), len(words)))
