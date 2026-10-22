#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored schwifty and prints expected.out.
mini_schwifty.kara must reproduce this byte-for-byte on every backend.

Each job is `<op>\t<iban>`:

  valid <iban>  -> VALID for a well-formed IBAN, else the SchwiftyException
                   message (invalid characters / unknown country / length /
                   BBAN structure / checksum);
  fmt   <iban>  -> IBAN.formatted, the compact IBAN in blocks of four;
  parts <iban>  -> "bank=<> branch=<> account=<>" from the BBAN components.
"""
import sys

sys.path.insert(0, "vendor")
from schwifty import IBAN, exceptions  # noqa: E402


def run(op, payload):
    if op == "valid":
        try:
            iban = IBAN(payload)
        except exceptions.SchwiftyException as e:
            return str(e)
        return "VALID " + iban.compact
    if op == "fmt":
        return IBAN(payload).formatted
    if op == "parts":
        i = IBAN(payload)
        return "bank=" + i.bank_code + " branch=" + i.branch_code + " account=" + i.account_code
    return "unknown op"


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        op, payload = line.split("\t", 1)
        chunks.append("== " + op + " " + payload + "\n  " + run(op, payload) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
