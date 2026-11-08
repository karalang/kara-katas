#!/usr/bin/env python3
"""Plays data/script.txt against the vendored multidict 7.2.1 (its pure
Python implementation) and prints the report mini_multidict.kara must
reproduce byte for byte (README.md has the rules).

Every message comes from the library or from Python, except the ones the
README marks as the port's own (a script word that does not parse, a name
the script never made). Python prints a set in hash order, which changes
from run to run, so a set is printed sorted.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import sys

sys.path.insert(0, "vendor")
import multidict  # noqa: E402
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy  # noqa: E402

KINDS = {"md": (MultiDict, MultiDictProxy), "ci": (CIMultiDict, CIMultiDictProxy)}
MUTATORS = ("add", "setdefault", "popone", "popall", "popitem", "clear",
            "extend", "update", "merge")


class Bad(Exception):
    """A problem the port reports in its own words."""


def text(word):
    """A script word as text: `\\s` is a space; every other character is
    itself."""
    return word.replace("\\s", " ")


def pairs(words):
    out = []
    for w in words:
        k, eq, v = w.partition("=")
        if not eq:
            raise Bad(f"bad pair {w}")
        out.append((text(k), text(v)))
    return out


def show_set(s):
    if not s:
        return "set()"
    return "{" + ", ".join(repr(x) for x in sorted(s)) + "}"


class Player:
    def __init__(self):
        self.objs = {}

    def obj(self, name):
        if name not in self.objs:
            raise Bad(f"no multidict {name}")
        return self.objs[name]

    def fresh(self, name):
        if name in self.objs:
            raise Bad(f"{name} exists")
        return name

    def source(self, words):
        """`from OTHER`, or `K=V` pairs."""
        if words[:1] == ["from"]:
            if len(words) != 2:
                raise Bad("usage: ... from OTHER")
            return self.obj(words[1])
        return pairs(words)

    def run(self, words):
        cmd, args = words[0], words[1:]
        if cmd == "new":
            if len(args) < 2 or args[1] not in KINDS:
                raise Bad("usage: new NAME md|ci [K=V ...] | new NAME md|ci from OTHER")
            name = self.fresh(args[0])
            src = self.source(args[2:])
            self.objs[name] = KINDS[args[1]][0](src)
            return []
        if cmd == "proxy":
            if len(args) != 3 or args[1] not in KINDS:
                raise Bad("usage: proxy NAME md|ci OF")
            name = self.fresh(args[0])
            target = self.obj(args[2])
            self.objs[name] = KINDS[args[1]][1](target)
            return []
        if cmd == "copy":
            if len(args) != 2:
                raise Bad("usage: copy NAME NEW")
            o = self.obj(args[0])
            self.objs[self.fresh(args[1])] = o.copy()
            return []
        if not args:
            raise Bad(f"usage: {cmd} NAME ...")
        o = self.obj(args[0])
        rest = args[1:]
        rest_t = [text(w) for w in rest]
        if cmd == "show":
            self.want(cmd, rest, 0, 0)
            return [repr(o)]
        if cmd == "len":
            self.want(cmd, rest, 0, 0)
            return [repr(len(o))]
        if cmd in ("keys", "values", "items"):
            self.want(cmd, rest, 0, 0)
            view = getattr(o, cmd)()
            return [f"{view!r} len {len(view)}"]
        if cmd == "reversed":
            if rest not in (["keys"], ["values"], ["items"]):
                raise Bad("usage: reversed NAME keys|values|items")
            return [repr(list(reversed(getattr(o, rest[0])())))]
        if cmd == "todict":
            self.want(cmd, rest, 0, 0)
            return [repr(o.to_dict())]
        if cmd == "has":
            self.want(cmd, rest, 1, 1)
            return [repr(rest_t[0] in o)]
        if cmd == "hasitem":
            self.want(cmd, rest, 2, 2)
            return [repr((rest_t[0], rest_t[1]) in o.items())]
        if cmd == "hasvalue":
            self.want(cmd, rest, 1, 1)
            return [repr(rest_t[0] in o.values())]
        if cmd == "item":
            self.want(cmd, rest, 1, 1)
            return [repr(o[rest_t[0]])]
        if cmd in ("get", "getone", "getall"):
            self.want(cmd, rest, 1, 2)
            return [repr(getattr(o, cmd)(*rest_t))]
        if cmd == "set":
            self.want(cmd, rest, 2, 2)
            o[rest_t[0]] = rest_t[1]
            return []
        if cmd == "del":
            self.want(cmd, rest, 1, 1)
            del o[rest_t[0]]
            return []
        if cmd == "eq":
            self.want(cmd, rest, 1, 1)
            return [repr(o == self.obj(rest[0]))]
        if cmd == "eqdict":
            return [repr(o == dict(pairs(rest)))]
        if cmd in ("keyset", "itemset"):
            return [self.setop(cmd, o, rest)]
        if cmd in MUTATORS:
            if cmd == "add" or cmd == "setdefault":
                self.want(cmd, rest, 2, 2)
            elif cmd in ("popone", "popall"):
                self.want(cmd, rest, 1, 2)
            elif cmd in ("popitem", "clear"):
                self.want(cmd, rest, 0, 0)
            method = getattr(o, cmd)
            if cmd in ("extend", "update", "merge"):
                method(self.source(rest))
                return []
            r = method(*rest_t)
            return [] if r is None else [repr(r)]
        raise Bad(f"unknown command {cmd}")

    def want(self, cmd, rest, lo, hi):
        if not lo <= len(rest) <= hi:
            n = f"{lo}" if lo == hi else f"{lo} or {hi}"
            raise Bad(f"{cmd} takes {n} word{'' if n == '1' else 's'} after the name")

    def setop(self, cmd, o, rest):
        if not rest:
            raise Bad(f"usage: {cmd} NAME OP [...]")
        op, words = rest[0], rest[1:]
        if cmd == "keyset":
            view, other = o.keys(), [text(w) for w in words]
        else:
            view, other = o.items(), pairs(words)
        if op == "and":
            return show_set(view & other)
        if op == "rand":
            return show_set(other & view)
        if op == "or":
            return show_set(view | other)
        if op == "ror":
            return show_set(other | view)
        if op == "sub":
            return show_set(view - other)
        if op == "rsub":
            return show_set(other - view)
        if op == "xor":
            return show_set(view ^ other)
        if op == "disjoint":
            return repr(view.isdisjoint(other))
        raise Bad(f"bad set operation {op}")


def main():
    with open(os.path.join("data", "script.txt"), encoding="utf-8", newline="") as fh:
        script = fh.read()
    player = Player()
    out = ["== mini_multidict " + multidict.__version__]
    for i, line in enumerate(script.split("\n")):
        words = line.split()
        if not words or words[0].startswith("#"):
            continue
        out.append("> " + " ".join(words))
        try:
            out.extend("  " + x for x in player.run(words))
        except Bad as e:
            out.append(f"  error: script.txt:{i + 1}: {e}")
        except (KeyError, TypeError, ValueError, AttributeError) as e:
            out.append(f"  error: script.txt:{i + 1}: {type(e).__name__}: {e}")
    out.append("== end")
    out.append(f"  {len(player.objs)} multidicts")
    sys.stdout.write("\n".join(out) + "\n")


main()
