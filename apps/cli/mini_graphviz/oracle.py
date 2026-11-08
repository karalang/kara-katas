#!/usr/bin/env python3
"""Plays data/script.txt against the vendored graphviz 0.21 and prints the
report mini_graphviz.kara must reproduce byte for byte (README.md has the
rules).

The library only writes DOT source here: nothing renders, so no Graphviz
binary is run. Every message comes from the library, except the ones the
README marks as the port's own (a script word that does not parse, a graph
the script never began, a command outside or inside a graph where it does
not belong). The library's DotSyntaxWarning is printed as a warning line,
and the address in a graph's repr is left out, since it differs from run
to run.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import re
import sys
import warnings

sys.path.insert(0, "vendor")
import graphviz  # noqa: E402

FILE = re.compile(r"^[a-z0-9_]+\.gv$")
ADDRESS = re.compile(r" at 0x[0-9a-fA-F]+>")
OUT = os.path.join("data", "out")


class Bad(Exception):
    """A problem the port reports in its own words."""


def text(word):
    """A script word as text: `\\s` is a space and `\\N` a newline; every
    other character, other backslashes included, is itself."""
    return word.replace("\\s", " ").replace("\\N", "\n")


def value(word):
    """A name or value: `!` first makes it nohtml, `%` first escapes it."""
    if word.startswith("!"):
        return graphviz.nohtml(text(word[1:]))
    if word.startswith("%"):
        return graphviz.escape(text(word[1:]))
    return text(word)


def pairs(words):
    """`K=V` words as a plain dict, which the library sorts by key."""
    out = {}
    for w in words:
        k, eq, v = w.partition("=")
        if not eq:
            raise Bad(f"bad attribute {w}")
        out[text(k)] = value(v)
    return out


def options(words, allow_strict):
    """The options of `begin` and `subgraph`."""
    kw = {"graph_attr": {}, "node_attr": {}, "edge_attr": {}}
    for w in words:
        if w == "strict" and allow_strict:
            kw["strict"] = True
            continue
        k, eq, v = w.partition("=")
        if not eq:
            raise Bad(f"bad option {w}")
        if k in ("name", "comment"):
            if k in kw:
                raise Bad(f"repeated option {k}")
            kw[k] = value(v)
            continue
        kind, dot, key = k.partition(".")
        if dot and kind in ("graph", "node", "edge"):
            kw[f"{kind}_attr"][text(key)] = value(v)
            continue
        raise Bad(f"bad option {w}")
    return kw


class Player:
    def __init__(self):
        self.docs = {}  # key -> graph, in the order they were made
        self.stack = []  # [(key or None, graph, context manager or None)]

    def current(self, cmd):
        if not self.stack:
            raise Bad(f"{cmd} needs an open graph")
        return self.stack[-1][1]

    def doc(self, key):
        if key not in self.docs:
            raise Bad(f"no graph {key}")
        return self.docs[key]

    def run(self, words):
        cmd = words[0]
        if cmd == "begin":
            if self.stack:
                raise Bad(f"begin inside {self.stack[0][0]}")
            if len(words) < 3 or words[2] not in ("graph", "digraph"):
                raise Bad("usage: begin KEY graph|digraph [OPTION ...]")
            key = words[1]
            if key in self.docs:
                raise Bad(f"graph {key} exists")
            kw = options(words[3:], True)
            cls = graphviz.Graph if words[2] == "graph" else graphviz.Digraph
            self.stack.append((key, cls(**kw), None))
            return []
        if cmd == "subgraph":
            parent = self.current(cmd)
            kw = options(words[1:], False)
            cm = parent.subgraph(**kw)
            sub = cm.__enter__()
            self.stack.append((None, sub, cm))
            return []
        if cmd == "end":
            if len(words) != 1:
                raise Bad("usage: end")
            if not self.stack:
                raise Bad("end needs an open graph")
            key, g, cm = self.stack.pop()
            if cm is not None:
                cm.__exit__(None, None, None)
                return []
            self.docs[key] = g
            return [f"  built {key}: {len(g.body)} body lines"]
        if cmd == "node":
            g = self.current(cmd)
            if len(words) < 2:
                raise Bad("usage: node NAME [K=V ...]")
            attrs = pairs(words[2:])
            label = attrs.pop("label", None)
            g.node(value(words[1]), label, _attributes=attrs)
            return []
        if cmd == "edge":
            g = self.current(cmd)
            if len(words) < 3:
                raise Bad("usage: edge TAIL HEAD [K=V ...]")
            attrs = pairs(words[3:])
            label = attrs.pop("label", None)
            g.edge(value(words[1]), value(words[2]), label, _attributes=attrs)
            return []
        if cmd == "edges":
            g = self.current(cmd)
            ends = words[1:]
            if not ends or len(ends) % 2:
                raise Bad("usage: edges TAIL HEAD [TAIL HEAD ...]")
            g.edges([(value(ends[i]), value(ends[i + 1])) for i in range(0, len(ends), 2)])
            return []
        if cmd == "attr":
            g = self.current(cmd)
            rest = words[1:]
            kw = None
            if rest and "=" not in rest[0]:
                kw = rest.pop(0)
            g.attr(kw, _attributes=pairs(rest))
            return []
        if cmd == "include":
            g = self.current(cmd)
            if len(words) != 2:
                raise Bad("usage: include KEY")
            g.subgraph(self.doc(words[1]))
            return []
        if cmd in ("print", "copy", "clear", "save"):
            if self.stack:
                raise Bad(f"{cmd} inside {self.stack[0][0]}")
        if cmd == "print":
            if len(words) != 2:
                raise Bad("usage: print KEY")
            src = self.doc(words[1]).source
            return ["  " + line for line in src.split("\n")[:-1]]
        if cmd == "copy":
            if len(words) != 3:
                raise Bad("usage: copy KEY NEW")
            g = self.doc(words[1])
            if words[2] in self.docs:
                raise Bad(f"graph {words[2]} exists")
            self.docs[words[2]] = g.copy()
            return []
        if cmd == "clear":
            if len(words) not in (2, 3) or words[2:] not in ([], ["keep"]):
                raise Bad("usage: clear KEY [keep]")
            self.doc(words[1]).clear(keep_attrs=words[2:] == ["keep"])
            return []
        if cmd == "save":
            if len(words) != 3:
                raise Bad("usage: save KEY FILE")
            g = self.doc(words[1])
            if not FILE.match(words[2]):
                raise Bad(f"bad file name {words[2]}")
            path = g.save(filename=words[2], directory=OUT)
            with open(path, "rb") as fh:
                data = fh.read()
            lines = data.decode("utf-8").split("\n")[:-1]
            return [f"  saved out/{words[2]}: {len(lines)} lines, {len(data)} bytes"] + \
                ["  " + line for line in lines]
        raise Bad(f"unknown command {cmd}")


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join("data", "script.txt"), encoding="utf-8", newline="") as fh:
        script = fh.read()
    player = Player()
    out = ["== mini_graphviz"]
    for i, line in enumerate(script.split("\n")):
        words = line.split()
        if not words or words[0].startswith("#"):
            continue
        out.append("> " + " ".join(words))
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                lines = player.run(words)
            except (Bad, ValueError) as e:
                lines = [f"  error: script.txt:{i + 1}: {ADDRESS.sub('>', str(e))}"]
        for w in caught:
            out.append(f"  warning: script.txt:{i + 1}: {w.message}")
        out.extend(lines)
    out.append("== end")
    out.append(f"  {len(player.docs)} graphs built")
    sys.stdout.write("\n".join(out) + "\n")


main()
