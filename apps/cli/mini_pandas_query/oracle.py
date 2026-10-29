"""The oracle for mini_pandas_query: runs every job in data/jobs.txt on
pandas itself and prints the transcript mini_pandas_query.kara must
print. For each job: `$ <job>`, then what the job's last step prints, or
the error pandas raised after `! `.

`query` is DataFrame.query and `eval` DataFrame.eval, both with
local_dict holding the job's `let` values and an empty global_dict, so
that `@name` sees only what the job defined. numexpr is not installed,
so pandas evaluates with its python engine. In `eval`, ` ; ` separates
the lines of a multi-line expression.

print(df) is printed with display.max_columns at 20, its value outside a
terminal.

Needs pandas 3.0.5 on numpy, with none of numexpr, bottleneck or pyarrow
installed.

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
    if tok.startswith("[") and tok.endswith("]"):
        inner = tok[1:-1]
        return [literal(p) for p in inner.split(",")] if inner else []
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


def step(obj, op, toks):
    pos, kw = split_args(toks)
    if op == "select":
        return obj[[text(n) for n in names(pos[0])]]
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
    if op == "setidx":
        return obj.set_index(names(pos[0]))
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
    local = {}
    for s in steps[1:]:
        op, _, rest = s.partition(" ")
        if op == "let":
            for t in rest.split(" "):
                k, v = t.split("=", 1)
                local[k] = literal(v)
            continue
        if op == "query":
            obj = obj.query(rest, local_dict=local, global_dict={})
            continue
        if op == "eval":
            obj = obj.eval(rest.replace(" ; ", "\n"), local_dict=local, global_dict={})
            continue
        toks = s.split(" ")
        _, kw = split_args(toks[1:])
        if op == "show":
            return show(obj, kw)
        if op == "string":
            return to_string(obj, kw)
        obj = step(obj, op, toks[1:])
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return show(obj, {})
    return repr(obj)


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
