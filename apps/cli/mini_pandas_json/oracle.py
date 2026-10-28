"""The oracle for mini_pandas_json: runs every job in data/jobs.txt on pandas
itself and prints the transcript mini_pandas_json.kara must print. For each
job: `$ <job>`, then the result frame as `to_csv` writes it, or the error
pandas raised after `! `.

Needs pandas 3.0.5 on numpy, with neither bottleneck nor pyarrow installed
(both change which kernels and string arrays pandas uses).

Run: python3 -I -B oracle.py > expected.out"""
import json
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
warnings.simplefilter("ignore")


def literal(tok):
    """A value written in a job: 'text', an int, or a float."""
    if tok.startswith("'") and tok.endswith("'"):
        return tok[1:-1]
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        return tok


def split_args(toks):
    pos, kw = [], {}
    for t in toks:
        if "=" in t and not t.startswith("=") and t != "==":
            k, v = t.split("=", 1)
            kw[k] = v
        else:
            pos.append(t)
    return pos, kw


def names(s):
    return s.split(",") if s else []


def literal_number(tok):
    try:
        return int(tok)
    except ValueError:
        return float(tok)


OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
}


def normalize(data, kw):
    """pd.json_normalize with the options a job names. A meta path and a
    record path are written with dots between their keys."""
    opts = {}
    if "record_path" in kw:
        opts["record_path"] = kw["record_path"].replace(",", ".").split(".")
    if "meta" in kw:
        opts["meta"] = [m.split(".") if "." in m else m for m in names(kw["meta"])]
    for k in ("sep", "record_prefix", "meta_prefix", "errors"):
        if k in kw:
            opts[k] = kw[k]
    if "max_level" in kw:
        opts["max_level"] = int(kw["max_level"])
    return pd.json_normalize(data, **opts)


def read(kind, path, kw):
    if kind == "read":
        return pd.read_csv(os.path.join("data", path))
    with open(os.path.join("data", path), encoding="utf-8") as f:
        text = f.read()
    if kind == "json":
        data = json.loads(text)
    else:
        data = [json.loads(line) for line in text.splitlines() if line.strip()]
    return normalize(data, kw)


def bins_arg(tok):
    """An int is a number of bins; a list is the edges."""
    if "," in tok:
        return [literal_number(t) for t in names(tok)]
    return int(tok)


def step(df, op, toks):
    """One step of a job applied to the frame."""
    pos, kw = split_args(toks)
    if op == "dtypes":
        return pd.DataFrame({"column": list(df.columns), "dtype": [str(t) for t in df.dtypes]})
    if op == "head":
        return df.head(int(pos[0]))
    if op == "tail":
        return df.tail(int(pos[0]))
    if op == "select":
        return df[names(pos[0])]
    if op == "drop":
        return df.drop(columns=names(pos[0]))
    if op == "where":
        col, rel, rhs = toks
        return df[OPS[rel](df[col], literal(rhs))]
    if op == "round":
        df = df.copy()
        df[pos[0]] = df[pos[0]].round(int(pos[1]))
        return df
    if op == "len":
        df = df.copy()
        df[pos[1]] = df[pos[0]].str.len()
        return df
    if op == "sort":
        by = names(pos[0])
        asc = [a == "1" for a in names(kw["asc"])] if "asc" in kw else True
        if isinstance(asc, list) and len(asc) == 1:
            asc = asc[0]
        return df.sort_values(by=by, ascending=asc, kind="stable")
    if op == "dedup":
        return df.drop_duplicates(subset=names(pos[0]))
    if op == "agg":
        keys = names(pos[0])
        spec = {}
        for p in names(pos[1]):
            c, f = p.split(":")
            spec[f"{c}_{f}"] = (c, f)
        return df.groupby(keys).agg(**spec).reset_index()
    if op == "counts":
        return df[pos[0]].value_counts().reset_index()
    if op == "explode":
        return df.explode(pos[0])
    if op == "split":
        df = df.copy()
        df[pos[0]] = df[pos[0]].str.split(pos[1])
        return df
    if op == "splitx":
        col, sep, new = pos
        new = names(new)
        parts = df[col].str.split(sep, n=len(new) - 1, expand=True)
        df = df.copy()
        for i, name in enumerate(new):
            df[name] = parts[i]
        return df
    if op == "dummies":
        return df.join(df[pos[0]].str.get_dummies(sep=pos[1]))
    if op == "getdummies":
        return pd.get_dummies(df, columns=[pos[0]], prefix=kw.get("prefix"))
    if op == "cut":
        col, bins, new = pos
        opts = {"right": kw.get("right", "1") == "1", "include_lowest": kw.get("lowest", "0") == "1"}
        if "labels" in kw:
            opts["labels"] = names(kw["labels"])
        df = df.copy()
        df[new] = pd.cut(df[col], bins_arg(bins), **opts)
        return df
    if op == "qcut":
        col, q, new = pos
        opts = {}
        if "labels" in kw:
            opts["labels"] = names(kw["labels"])
        df = df.copy()
        df[new] = pd.qcut(df[col], bins_arg(q), **opts)
        return df
    if op == "cat":
        cats = [c.replace("_", " ") for c in names(pos[1])]
        df = df.copy()
        df[pos[0]] = df[pos[0]].astype(pd.CategoricalDtype(cats, ordered=kw.get("ordered") == "1"))
        return df
    if op == "nlargest":
        return df.nlargest(int(pos[0]), pos[1])
    if op == "nsmallest":
        return df.nsmallest(int(pos[0]), pos[1])
    if op == "interpolate":
        df = df.copy()
        df[pos[0]] = df[pos[0]].interpolate()
        return df
    if op == "cumcount":
        df = df.copy()
        df[pos[0]] = df.groupby(names(kw["by"])).cumcount()
        return df
    if op == "ngroup":
        df = df.copy()
        df[pos[0]] = df.groupby(names(kw["by"])).ngroup()
        return df
    if op == "replace":
        df = df.copy()
        df[pos[0]] = df[pos[0]].replace(pos[1], pos[2])
        return df
    raise ValueError(f"unknown step {op}")


def run(line):
    steps = line.split(" | ")
    first = steps[0].split(" ")
    pos, kw = split_args(first[1:])
    df = read(first[0], pos[0], kw)
    for s in steps[1:]:
        toks = s.split(" ")
        df = step(df, toks[0], toks[1:])
    return df.to_csv(index=False, lineterminator="\n")


def main():
    os.chdir(HERE)
    with open(os.path.join(DATA, "jobs.txt"), encoding="utf-8") as f:
        jobs = [l.rstrip("\n") for l in f if l.strip()]
    out = []
    for line in jobs:
        out.append(f"$ {line}\n")
        try:
            out.append(run(line))
        except Exception as e:  # what pandas raised is part of the transcript
            out.append(f"! {type(e).__name__}: {e}\n")
    sys.stdout.write("".join(out))


main()
