"""The oracle for mini_pandas_io: runs every job in data/jobs.txt on
pandas itself and prints the transcript mini_pandas_io.kara must print.
For each job: `$ <job>`, then each ParserWarning line after `~ `, then
the frame as `to_csv(index=False)` writes it (with the options of a
final `write` step), or the error pandas raised after `! `, its trailing
newline dropped.

Needs pandas 3.0.5 on numpy, with neither bottleneck nor pyarrow installed
(both change which kernels and string arrays pandas uses).

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def literal(tok):
    """A value written in a job: 'text', an int, or a float."""
    if tok.startswith("'") and tok.endswith("'") and len(tok) >= 2:
        return tok[1:-1]
    if tok in ("True", "False"):
        return tok == "True"
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        return tok


def text(tok):
    """A text argument: \\s is a space, \\t a tab, \\e the empty string."""
    return "" if tok == "\\e" else tok.replace("\\s", " ").replace("\\t", "\t")


OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
}


def split_args(toks):
    pos, kw = [], {}
    for t in toks:
        if "=" in t and not t.startswith("=") and t not in OPS:
            k, v = t.split("=", 1)
            kw[k] = v
        else:
            pos.append(t)
    return pos, kw


def names(s):
    return s.split(",") if s else []


def read(path, kw):
    """read_csv with the options a job names."""
    o = {}
    if "sep" in kw:
        o["sep"] = r"\s+" if kw["sep"] == "ws" else text(kw["sep"])
    if kw.get("header") == "none":
        o["header"] = None
    if "names" in kw:
        o["names"] = names(kw["names"])
    if "skiprows" in kw:
        o["skiprows"] = int(kw["skiprows"])
    if "skiplines" in kw:
        o["skiprows"] = [int(x) for x in names(kw["skiplines"])]
    if "nrows" in kw:
        o["nrows"] = int(kw["nrows"])
    for k in ("comment", "quotechar", "escapechar", "decimal", "thousands", "on_bad_lines"):
        if k in kw:
            o[k] = text(kw[k])
    for k in ("doublequote", "skipinitialspace", "keep_default_na", "skip_blank_lines"):
        if k in kw:
            o[k] = kw[k] == "1"
    if "quoting" in kw:
        o["quoting"] = int(kw["quoting"])
    if "na" in kw:
        o["na_values"] = names(kw["na"])
    if "true" in kw:
        o["true_values"] = names(kw["true"])
    if "false" in kw:
        o["false_values"] = names(kw["false"])
    if "usecols" in kw:
        o["usecols"] = names(kw["usecols"])
    if "dtype" in kw:
        o["dtype"] = dict(p.split(":") for p in names(kw["dtype"]))
    return pd.read_csv(os.path.join("data", path), **o)


def write(df, toks):
    """to_csv(index=False) with the options of a `write` step."""
    _, kw = split_args(toks)
    o = {"index": False, "lineterminator": "\n"}
    if "sep" in kw:
        o["sep"] = text(kw["sep"])
    if "na" in kw:
        o["na_rep"] = text(kw["na"])
    if "float" in kw:
        o["float_format"] = kw["float"]
    if "quoting" in kw:
        o["quoting"] = int(kw["quoting"])
    for k in ("quotechar", "escapechar", "decimal"):
        if k in kw:
            o[k] = text(kw[k])
    if "doublequote" in kw:
        o["doublequote"] = kw["doublequote"] == "1"
    if "header" in kw:
        o["header"] = kw["header"] == "1"
    if "columns" in kw:
        o["columns"] = names(kw["columns"])
    return df.to_csv(**o)


def step(df, op, toks):
    """One step of a job applied to the frame."""
    pos, kw = split_args(toks)
    if op == "dtypes":
        return pd.DataFrame({"column": [str(c) for c in df.columns], "dtype": [str(t) for t in df.dtypes]})
    if op == "head":
        return df.head(int(pos[0]))
    if op == "select":
        return df[names(pos[0])]
    if op == "where":
        col, rel, rhs = toks
        return df[OPS[rel](df[col], literal(rhs))]
    if op == "agg":
        keys = names(toks[0])
        spec = {}
        for p in names(toks[1]):
            out, rest = p.split("=")
            c, f = rest.split(":")
            spec[out] = (c, f)
        return df.groupby(keys).agg(**spec).reset_index()
    if op == "dropna":
        o = {}
        if "how" in kw:
            o["how"] = kw["how"]
        if "thresh" in kw:
            o["thresh"] = int(kw["thresh"])
        if "subset" in kw:
            o["subset"] = names(kw["subset"])
        return df.dropna(**o)
    if op == "dedup":
        keep = kw.get("keep", "first")
        return df.drop_duplicates(subset=names(kw["subset"]) if "subset" in kw else None,
                                  keep=False if keep == "False" else keep)
    if op == "rename":
        m = {}
        for p in names(pos[0]):
            a, b = p.rsplit(":", 1)
            m[text(a)] = text(b)
        return df.rename(columns=m)
    df = df.copy()
    col = pos[0]
    s = df[col]
    out = kw.get("as", col)
    limit = int(kw["limit"]) if "limit" in kw else None
    if op in ("ffill", "bfill"):
        if "by" in kw:
            df[out] = getattr(df.groupby(kw["by"])[col], op)(limit=limit)
        else:
            df[out] = getattr(s, op)(limit=limit)
    elif op == "fillna":
        df[out] = s.fillna(literal(pos[1]))
    elif op == "shift":
        df[out] = s.shift(int(pos[1]))
    elif op == "diff":
        df[out] = s.diff(int(kw.get("periods", "1")))
    elif op == "pct_change":
        df[out] = s.pct_change()
    elif op in ("cumsum", "cumprod", "cummax", "cummin"):
        df[out] = getattr(s, op)()
    elif op == "clip":
        df[out] = s.clip(lower=literal(kw["lower"]) if "lower" in kw else None,
                         upper=literal(kw["upper"]) if "upper" in kw else None)
    elif op == "round":
        df[out] = s.round(int(pos[1]))
    elif op == "replace":
        df[out] = s.replace(literal(pos[1]), literal(pos[2]))
    elif op == "astype":
        df[out] = s.astype(pos[1])
    elif op == "strip":
        df[out] = s.str.strip()
    else:
        raise ValueError(f"unknown step {op}")
    return df


def run(line):
    steps = line.split(" | ")
    first = steps[0].split(" ")
    assert first[0] == "read"
    pos, kw = split_args(first[1:])
    warns = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        df = read(pos[0], kw)
    for w in caught:
        for l in str(w.message).splitlines():
            warns.append(f"~ {type(w.message).__name__}: {l}\n")
    for s in steps[1:]:
        toks = s.split(" ")
        if toks[0] == "write":
            return "".join(warns) + write(df, toks[1:])
        df = step(df, toks[0], toks[1:])
    return "".join(warns) + df.to_csv(index=False, lineterminator="\n")


def main():
    os.chdir(HERE)
    warnings.simplefilter("ignore")
    with open(os.path.join(DATA, "jobs.txt"), encoding="utf-8") as f:
        jobs = [l.rstrip("\n") for l in f if l.strip()]
    out = []
    for line in jobs:
        out.append(f"$ {line}\n")
        try:
            out.append(run(line))
        except Exception as e:  # what pandas raised is part of the transcript
            msg = str(e).rstrip("\n")
            out.append(f"! {type(e).__name__}: {msg}\n")
    sys.stdout.write("".join(out))


main()
