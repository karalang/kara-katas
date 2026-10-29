"""The oracle for mini_pandas_display: runs every job in data/jobs.txt on
pandas itself and prints the transcript mini_pandas_display.kara must
print. For each job: `$ <job>`, then what the job's last step prints, or
the error pandas raised after `! `.

print(df) is printed with display.max_columns at 20, its value outside a
terminal (in a notebook, or with output going to a file or a pipe);
inside a terminal pandas sizes the frame to the window instead.

Needs pandas 3.0.5 on numpy, with neither bottleneck nor pyarrow
installed (both change which kernels and string arrays pandas uses), and
tabulate 0.10.0 for to_markdown.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

pd.set_option("display.max_columns", 20)


def literal(tok):
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
    """A text argument: \\s is a space, \\e the empty string."""
    return "" if tok == "\\e" else tok.replace("\\s", " ")


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


def flag(v):
    return v not in ("0", "False")


def opt_int(v):
    return None if v == "None" else int(v)


def read(pos, kw):
    o = {}
    if "sep" in kw:
        o["sep"] = text(kw["sep"])
    if "index" in kw:
        o["index_col"] = names(kw["index"])
    if "dtype" in kw:
        o["dtype"] = dict(p.split(":") for p in names(kw["dtype"]))
    return pd.read_csv(os.path.join(DATA, pos[0]), **o)


def aggspec(s):
    out = {}
    for p in names(s):
        k, v = p.split("=")
        col, fn = v.split(":")
        out[k] = (col, fn)
    return out


def step(obj, op, toks):
    pos, kw = split_args(toks)
    if op == "select":
        return obj[names(pos[0])]
    if op == "where":
        return obj[OPS[pos[1]](obj[pos[0]], literal(pos[2]))]
    if op == "head":
        return obj.head(int(pos[0]))
    if op == "tail":
        return obj.tail(int(pos[0]))
    if op == "sort":
        asc = [flag(x) for x in names(kw.get("asc", "1"))]
        if isinstance(obj, pd.Series):
            return obj.sort_values(ascending=asc[0], kind="stable")
        by = names(kw["by"])
        return obj.sort_values(by, ascending=asc if len(asc) > 1 else asc[0], kind="stable")
    if op == "sortidx":
        return obj.sort_index(ascending=flag(kw.get("asc", "1")))
    if op == "setidx":
        return obj.set_index(names(pos[0]))
    if op == "reset":
        return obj.reset_index()
    if op == "agg":
        return obj.groupby(names(toks[0])).agg(**aggspec(toks[1]))
    if op == "size":
        return obj.groupby(names(pos[0])).size()
    if op == "pivot":
        o = {"index": names(kw["index"]), "columns": names(kw["columns"])}
        if "values" in kw:
            o["values"] = names(kw["values"])
        aggs = names(kw.get("agg", "mean"))
        o["aggfunc"] = aggs if len(aggs) > 1 else aggs[0]
        if "fill" in kw:
            o["fill_value"] = literal(kw["fill"])
        if "margins" in kw:
            o["margins"] = flag(kw["margins"])
        return obj.pivot_table(**o)
    if op == "unstack":
        return obj.unstack()
    if op == "stack":
        return obj.stack()
    if op == "T":
        return obj.T
    if op == "describe":
        return obj.describe()
    if op == "counts":
        return obj[pos[0]].value_counts()
    if op == "share":
        return obj[pos[0]].value_counts(normalize=True)
    if op == "col":
        return obj[pos[0]]
    if op == "round":
        return obj.round(int(pos[0]))
    if op == "mul":
        obj = obj.copy()
        obj[pos[0]] = obj[pos[0]] * literal(pos[1])
        return obj
    if op == "div":
        obj = obj.copy()
        obj[pos[0]] = obj[pos[1]] / obj[pos[2]]
        return obj
    raise ValueError(f"unknown step {op}")


SHOW = {
    "max_rows": opt_int, "min_rows": opt_int, "max_columns": opt_int,
    "width": int, "precision": int, "max_colwidth": opt_int,
    "show_dimensions": lambda v: v if v == "truncate" else flag(v),
    "colheader_justify": str, "multi_sparse": flag,
    "expand_frame_repr": flag,
}


def show(obj, kw):
    args = []
    for k, v in kw.items():
        args += [f"display.{k}", SHOW[k](v)]
    if args:
        with pd.option_context(*args):
            return repr(obj)
    return repr(obj)


STRING = {
    "index": flag, "header": flag, "na_rep": text, "float_format": text,
    "col_space": int, "justify": str, "sparsify": flag, "index_names": flag,
    "max_rows": opt_int, "min_rows": opt_int, "max_cols": opt_int,
    "show_dimensions": lambda v: v if v == "truncate" else flag(v),
    "decimal": text, "line_width": opt_int, "max_colwidth": opt_int,
    "length": flag, "dtype": flag, "name": flag,
}


def to_string(obj, kw):
    return obj.to_string(**{k: STRING[k](v) for k, v in kw.items()})


def run(line):
    steps = line.split(" | ")
    first = steps[0].split(" ")
    pos, kw = split_args(first[1:])
    obj = read(pos, kw)
    for s in steps[1:]:
        toks = s.split(" ")
        _, kw = split_args(toks[1:])
        if toks[0] == "show":
            return show(obj, kw)
        if toks[0] == "string":
            return to_string(obj, kw)
        obj = step(obj, toks[0], toks[1:])
    return show(obj, {})


def main():
    with open(os.path.join(DATA, "jobs.txt"), encoding="utf-8") as f:
        jobs = [l.rstrip("\n") for l in f if l.strip()]
    out = []
    for line in jobs:
        out.append(f"$ {line}")
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                out.append(run(line))
        except Exception as e:
            out.append(f"! {type(e).__name__}: {str(e).rstrip()}")
    sys.stdout.write("\n".join(out) + "\n")


main()
