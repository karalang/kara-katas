#!/usr/bin/env python3
"""Plays data/script.txt against the vendored `netrc` module (CPython
3.13's Lib/netrc.py) and prints the report mini_netrc.kara must reproduce
byte for byte (README.md has the rules).

The files are passed by path, so the module's ~/.netrc ownership and
permission check never runs. Every message comes from the module, except
the ones the README marks as the port's own.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys

sys.path.insert(0, "vendor")
import netrc  # noqa: E402

USAGE = {
    "parse": "usage: parse NAME",
    "dump": "usage: dump NAME",
    "auth": "usage: auth NAME HOST",
    "macro": "usage: macro NAME MACRO",
}


class Bad(Exception):
    """A problem the port reports in its own words."""


class Player:
    def __init__(self):
        self.parsed = {}

    def get(self, name):
        if name not in self.parsed:
            raise Bad(f"{name} is not parsed")
        return self.parsed[name]

    def run(self, words):
        cmd = words[0]
        if cmd not in USAGE:
            raise Bad(f"unknown command {cmd}")
        if len(words) != len(USAGE[cmd].split()) - 1:
            raise Bad(USAGE[cmd])
        if cmd == "parse":
            path = os.path.join("data", words[1] + ".netrc")
            self.parsed.pop(words[1], None)
            if not os.path.exists(path):
                raise Bad(f"no file {path}")
            n = netrc.netrc(path)
            self.parsed[words[1]] = n
            return [f"parsed {path}: {len(n.hosts)} hosts, {len(n.macros)} macros"]
        n = self.get(words[1])
        if cmd == "dump":
            return ["| " + line for line in repr(n).split("\n")[:-1]]
        if cmd == "auth":
            return [repr(n.authenticators(words[2]))]
        if words[2] not in n.macros:
            raise Bad(f"no macro {words[2]}")
        return [repr(n.macros[words[2]])]


def main():
    with open(os.path.join("data", "script.txt"), encoding="utf-8", newline="") as fh:
        script = fh.read()
    player = Player()
    out = ["== mini_netrc"]
    for i, line in enumerate(script.split("\n")):
        words = line.split()
        if not words or words[0].startswith("#"):
            continue
        out.append("> " + " ".join(words))
        try:
            out.extend("  " + x for x in player.run(words))
        except Bad as e:
            out.append(f"  error: script.txt:{i + 1}: {e}")
        except netrc.NetrcParseError as e:
            out.append(f"  error: script.txt:{i + 1}: NetrcParseError: {e}")
    out.append("== end")
    out.append(f"  {len(player.parsed)} files parsed")
    sys.stdout.write("\n".join(out) + "\n")


main()
