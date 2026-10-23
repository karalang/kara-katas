"""Replay data/jobs.tsv against the vendored zxcvbn 4.5.0.

`check` runs zxcvbn() on a password (with optional user inputs and a
`max_length=` override) and prints its guesses, score, crack times, the
match sequence it settled on and its feedback. `matches` prints every
candidate match omnimatch finds, `subs` the l33t substitution tables
tried for a password, and `time` the attack-time estimates for a guess
count. A job that raises prints `error <class>: <message>`.

zxcvbn keeps the last call's user inputs in its module-level dictionary
table, so a `matches` job sees the inputs of the `check` before it, as a
caller of the library would.
"""
import os
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))

from zxcvbn import zxcvbn  # noqa: E402
from zxcvbn import matching, time_estimates  # noqa: E402


def out(s):
    print("  " + s)


def unescape(s):
    """Job text uses \\t, \\n, \\\\ and \\uXXXX escapes."""
    res = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "t":
                res.append("\t")
            elif n == "n":
                res.append("\n")
            elif n == "u":
                res.append(chr(int(s[i + 2:i + 6], 16)))
                i += 4
            else:
                res.append(n)
            i += 2
            continue
        res.append(c)
        i += 1
    return "".join(res)


def field(m, key):
    v = m[key]
    if isinstance(v, str):
        return repr(v)
    return str(v) if not isinstance(v, float) else repr(v)


EXTRA = {
    "dictionary": ["matched_word", "rank", "dictionary_name", "reversed",
                   "l33t"],
    "spatial": ["graph", "turns", "shifted_count"],
    "repeat": ["base_token", "base_guesses", "repeat_count"],
    "sequence": ["sequence_name", "sequence_space", "ascending"],
    "regex": ["regex_name"],
    "date": ["separator", "year", "month", "day"],
    "bruteforce": [],
}

SCORED = {
    "dictionary": ["base_guesses", "uppercase_variations", "l33t_variations"],
}


def describe(m, scored):
    parts = ["%s %d-%d %s" % (m["pattern"], m["i"], m["j"],
                              repr(m["token"]))]
    for key in EXTRA[m["pattern"]]:
        parts.append("%s=%s" % (key, field(m, key)))
    if m.get("l33t"):
        parts.append("sub=%s" % repr(m["sub_display"]))
    if m["pattern"] == "repeat":
        parts.append("base=[%s]" % ", ".join(
            "%s %s" % (b["pattern"], repr(b["token"]))
            for b in m["base_matches"]))
    if scored:
        for key in SCORED.get(m["pattern"], []):
            parts.append("%s=%s" % (key, field(m, key)))
        parts.append("guesses=%s" % field(m, "guesses"))
        parts.append("log10=%r" % m["guesses_log10"])
    return " ".join(parts)


def cmd_check(f):
    password = unescape(f[0])
    inputs = []
    max_length = None
    for x in f[1:]:
        if x.startswith("max_length="):
            max_length = int(x[len("max_length="):])
        elif x.startswith("int:"):
            inputs.append(int(x[4:]))
        else:
            inputs.append(unescape(x))
    if max_length is None:
        r = zxcvbn(password, user_inputs=inputs)
    else:
        r = zxcvbn(password, user_inputs=inputs, max_length=max_length)
    out("guesses %s log10 %r score %d" % (r["guesses"], r["guesses_log10"],
                                          r["score"]))
    for scenario, seconds in r["crack_times_seconds"].items():
        out("%s %s (%s)" % (scenario, seconds,
                            r["crack_times_display"][scenario]))
    out("sequence of %d" % len(r["sequence"]))
    for m in r["sequence"]:
        out("  " + describe(m, True))
    out("warning %r" % r["feedback"]["warning"])
    for s in r["feedback"]["suggestions"]:
        out("suggest %r" % s)


def cmd_matches(f):
    ms = matching.omnimatch(unescape(f[0]))
    out("%d matches" % len(ms))
    for m in ms:
        out("  " + describe(m, False))


def cmd_subs(f):
    password = unescape(f[0])
    table = matching.relevant_l33t_subtable(password, matching.L33T_TABLE)
    out("table %s" % " ".join("%s:%s" % (k, "".join(v))
                              for k, v in table.items()))
    subs = matching.enumerate_l33t_subs(table)
    out("%d subs" % len(subs))
    for sub in subs:
        out("  " + (" ".join("%s>%s" % (k, v) for k, v in sub.items())
                    or "-"))


def cmd_time(f):
    t = time_estimates.estimate_attack_times(Decimal(f[0]))
    out("score %d" % t["score"])
    for scenario, seconds in t["crack_times_seconds"].items():
        out("%s %s (%s)" % (scenario, seconds,
                            t["crack_times_display"][scenario]))


COMMANDS = {"check": cmd_check, "matches": cmd_matches, "subs": cmd_subs,
            "time": cmd_time}


def main():
    with open("data/jobs.tsv", encoding="utf-8") as fh:
        jobs = [ln.rstrip("\n") for ln in fh if ln.strip()]
    for line in jobs:
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line.replace("\t", " "))
        f = line.split("\t")
        try:
            COMMANDS[f[0]](f[1:])
        except Exception as e:  # noqa: BLE001
            print("  error %s: %s" % (type(e).__name__, e))


main()
