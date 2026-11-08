#!/usr/bin/env python3
"""Plays data/script.txt against the vendored prometheus_client 0.26.0 and
prints the report mini_prometheus_client.kara must reproduce byte for byte
(README.md has the rules).

One CollectorRegistry holds every metric. `_created` series are off and
names follow the legacy (pre-UTF-8) rules, so nothing depends on the clock
or on the new quoting. Every message comes from the library, except the
ones the README marks as the port's own: a script word that does not parse,
a metric the script never defined, a command the metric's type does not
have, and the two library calls that would raise AttributeError (`set` on an
info and `reset` on a counter that still needs label values).

Run from this directory: python3 -I -B oracle.py > expected.out"""
import os
import re
import sys

sys.path.insert(0, "vendor")
from prometheus_client import (  # noqa: E402
    CollectorRegistry, Counter, Enum, Gauge, Histogram, Info, Summary,
    generate_latest, write_to_textfile,
)
from prometheus_client.metrics import disable_created_metrics  # noqa: E402
from prometheus_client.openmetrics.exposition import (  # noqa: E402
    generate_latest as generate_openmetrics,
)
from prometheus_client.registry import DuplicateTimeseries  # noqa: E402
from prometheus_client.validation import enable_legacy_validation  # noqa: E402

disable_created_metrics()
enable_legacy_validation()

WORKERS = 4
NUMBER = re.compile(r"^(-?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?|\+Inf|-Inf|NaN)$")
FILE = re.compile(r"^[a-z0-9_]+\.prom$")
KINDS = {
    "counter": Counter, "gauge": Gauge, "summary": Summary,
    "histogram": Histogram, "info": Info, "enum": Enum,
}
OPTIONS = {
    "counter": ["labels", "unit", "ns", "sub"],
    "gauge": ["labels", "unit", "ns", "sub"],
    "summary": ["labels", "unit", "ns", "sub"],
    "histogram": ["labels", "unit", "ns", "sub", "buckets"],
    "info": ["labels", "unit", "ns", "sub"],
    "enum": ["labels", "unit", "ns", "sub", "states"],
}
# The commands each type has, beyond remove, clear and unregister.
OPS = {
    "inc": ["counter", "gauge"], "dec": ["gauge"], "set": ["gauge", "info"],
    "observe": ["histogram", "summary"], "state": ["enum"], "reset": ["counter"],
}


class Bad(Exception):
    """A problem the port reports in its own words."""


def split_escaped(word):
    """Splits on commas that are not escaped, then decodes each part."""
    parts, cur, i = [], [], 0
    while i < len(word):
        c = word[i]
        if c == "\\":
            if i + 1 == len(word):
                raise Bad(f"bad escape in {word}")
            e = word[i + 1]
            if e == "\\":
                cur.append("\\")
            elif e == "n":
                cur.append("\n")
            elif e == "s":
                cur.append(" ")
            elif e == ",":
                cur.append(",")
            else:
                raise Bad(f"bad escape in {word}")
            i += 2
            continue
        if c == ",":
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    parts.append("".join(cur))
    return parts


def text(word):
    """A word that is one text: its escapes decoded, a bare comma kept."""
    return ",".join(split_escaped(word))


def number(word):
    if not NUMBER.match(word):
        raise Bad(f"bad number {word}")
    return float(word)


class Player:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.metrics = {}  # full name -> (type word, metric)

    def target(self, word):
        name, at, rest = word.partition("@")
        if name not in self.metrics:
            raise Bad(f"no metric {name}")
        kind, metric = self.metrics[name]
        values = split_escaped(rest) if at else None
        return name, kind, metric, values

    @staticmethod
    def child(metric, values):
        return metric if values is None else metric.labels(*values)

    def define(self, kind, words):
        if len(words) < 2 or words[1] == ":":
            raise Bad(f"usage: {kind} NAME [OPTION=VALUE ...] [: HELP]")
        name = words[1]
        opts, rest = {}, words[2:]
        while rest and rest[0] != ":":
            w = rest.pop(0)
            key, eq, value = w.partition("=")
            if not eq:
                raise Bad(f"bad option {w}")
            if key not in OPTIONS[kind]:
                raise Bad(f"{kind} has no option {key}")
            if key in opts:
                raise Bad(f"repeated option {key}")
            opts[key] = value
        doc = " ".join(text(w) for w in rest[1:])
        kwargs = {
            "labelnames": opts["labels"].split(",") if "labels" in opts else (),
            "namespace": opts.get("ns", ""),
            "subsystem": opts.get("sub", ""),
            "unit": opts.get("unit", ""),
            "registry": self.registry,
        }
        if "buckets" in opts:
            kwargs["buckets"] = [number(b) for b in opts["buckets"].split(",")]
        if kind == "enum":
            kwargs["states"] = opts["states"].split(",") if "states" in opts else []
        metric = KINDS[kind](name, doc, **kwargs)
        self.metrics[metric._name] = (kind, metric)
        return [f"  defined {kind} {metric._name}"]

    def op(self, cmd, words):
        if len(words) < 2:
            raise Bad(f"usage: {cmd} TARGET ...")
        name, kind, metric, values = self.target(words[1])
        if kind not in OPS[cmd]:
            raise Bad(f"{kind} {name} has no {cmd}")
        args = words[2:]
        if cmd in ("inc", "dec"):
            if len(args) > 1:
                raise Bad(f"usage: {cmd} TARGET [AMOUNT]")
            amount = number(args[0]) if args else 1.0
            getattr(self.child(metric, values), cmd)(amount)
        elif cmd == "set" and kind == "info":
            pairs = {}
            for w in args:
                k, eq, v = w.partition("=")
                if not eq:
                    raise Bad(f"bad pair {w}")
                pairs[k] = text(v)
            if values is None and metric._labelnames:
                raise Bad("info metric is missing label values")
            self.child(metric, values).info(pairs)
        elif cmd in ("set", "observe"):
            if len(args) != 1:
                raise Bad(f"usage: {cmd} TARGET VALUE")
            value = number(args[0])
            getattr(self.child(metric, values), cmd)(value)
        elif cmd == "state":
            if len(args) != 1:
                raise Bad("usage: state TARGET STATE")
            self.child(metric, values).state(args[0])
        elif cmd == "reset":
            if args:
                raise Bad("usage: reset TARGET")
            if values is None and metric._labelnames:
                raise Bad("counter metric is missing label values")
            self.child(metric, values).reset()
        return []

    def run(self, words):
        cmd = words[0]
        if cmd in KINDS:
            return self.define(cmd, words)
        if cmd in OPS:
            return self.op(cmd, words)
        if cmd == "remove":
            if len(words) != 2:
                raise Bad("usage: remove TARGET")
            name, kind, metric, values = self.target(words[1])
            metric.remove(*(values or ()))
            return []
        if cmd in ("clear", "unregister"):
            if len(words) != 2:
                raise Bad(f"usage: {cmd} NAME")
            name, kind, metric, values = self.target(words[1])
            if values is not None:
                raise Bad(f"usage: {cmd} NAME")
            if cmd == "clear":
                metric.clear()
            else:
                self.registry.unregister(metric)
                del self.metrics[name]
            return []
        if cmd == "target":
            pairs = {}
            for w in words[1:]:
                k, eq, v = w.partition("=")
                if not eq:
                    raise Bad(f"bad pair {w}")
                pairs[k] = text(v)
            self.registry.set_target_info(pairs)
            return []
        if cmd == "expose":
            if words[1:] == []:
                out = generate_latest(self.registry)
            elif words[1:] == ["openmetrics"]:
                out = generate_openmetrics(self.registry)
            else:
                raise Bad("usage: expose [openmetrics]")
            return ["  " + line for line in out.decode("utf-8").split("\n")[:-1]]
        if cmd == "write":
            if len(words) != 2:
                raise Bad("usage: write FILE")
            if not FILE.match(words[1]):
                raise Bad(f"bad file name {words[1]}")
            path = os.path.join("data", "out", words[1])
            write_to_textfile(path, self.registry)
            with open(path, "rb") as fh:
                data = fh.read()
            lines = data.decode("utf-8").split("\n")[:-1]
            return [f"  wrote out/{words[1]}: {len(lines)} lines, {len(data)} bytes"] + \
                ["  " + line for line in lines]
        if cmd == "parallel":
            if len(words) < 3 or words[2] not in OPS:
                raise Bad("usage: parallel N COMMAND ...")
            if not re.match(r"^[1-9][0-9]{0,5}$", words[1]):
                raise Bad(f"bad count {words[1]}")
            n = int(words[1])
            errors = []
            for _ in range(n):
                try:
                    self.op(words[2], words[2:])
                except (Bad, ValueError) as e:
                    errors.append(message(e))
            if not errors:
                return [f"  ran {n} times on {WORKERS} workers"]
            assert len(set(errors)) == 1 and len(errors) == n, errors
            raise Bad(f"{errors[0]} ({n} times)")
        raise Bad(f"unknown command {cmd}")


def message(e):
    if isinstance(e, DuplicateTimeseries):
        names = ", ".join(repr(d) for d in sorted(e.duplicates))
        return f"Duplicated timeseries in CollectorRegistry: {{{names}}}"
    return str(e)


def main():
    os.makedirs(os.path.join("data", "out"), exist_ok=True)
    with open(os.path.join("data", "script.txt"), encoding="utf-8", newline="") as fh:
        script = fh.read()
    player = Player()
    out = ["== mini_prometheus_client"]
    for i, line in enumerate(script.split("\n")):
        words = line.split()
        if not words or words[0].startswith("#"):
            continue
        out.append("> " + " ".join(words))
        try:
            out.extend(player.run(words))
        except (Bad, ValueError) as e:
            out.append(f"  error: script.txt:{i + 1}: {message(e)}")
    out.append("== end")
    out.append(f"  {len(player.metrics)} metrics registered")
    sys.stdout.write("\n".join(out) + "\n")


main()
