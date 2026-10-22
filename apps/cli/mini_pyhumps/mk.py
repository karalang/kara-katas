#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pyhumps: op \t identifier, one per line.

Each op names one of the library's conversions or predicates; the identifier
is the string to convert. Inputs are ordinary API-style field names — the
camel / snake / kebab / pascal forms a JSON (de)serializer meets — mixing
underscores, hyphens, embedded acronyms (API, HTTP, ID) and a few digits.
"""
import os

JOBS = [
    ("camelize", "user_id"),
    ("camelize", "first_name"),
    ("camelize", "api_response_code"),
    ("camelize", "is_active"),
    ("camelize", "already_camel"),
    ("camelize", "HTTP_status"),
    ("decamelize", "firstName"),
    ("decamelize", "apiResponseCode"),
    ("decamelize", "getHTTPResponseCode"),
    ("decamelize", "userID"),
    ("decamelize", "alreadySnake"),
    ("decamelize", "parseURLToPath"),
    ("pascalize", "user_id"),
    ("pascalize", "first_name"),
    ("pascalize", "api_response_code"),
    ("pascalize", "http_status_code"),
    ("kebabize", "first_name"),
    ("kebabize", "api_response_code"),
    ("kebabize", "firstName"),
    ("kebabize", "getHTTPResponseCode"),
    ("dekebabize", "first-name"),
    ("dekebabize", "api-response-code"),
    ("is_camelcase", "firstName"),
    ("is_camelcase", "first_name"),
    ("is_snakecase", "first_name"),
    ("is_snakecase", "firstName"),
    ("is_pascalcase", "FirstName"),
    ("is_pascalcase", "firstName"),
    ("is_kebabcase", "first-name"),
    ("is_kebabcase", "first_name"),
]

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for op, arg in JOBS:
        fh.write("%s\t%s\n" % (op, arg))
