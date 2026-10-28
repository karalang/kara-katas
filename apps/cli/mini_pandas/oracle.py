"""The oracle for mini_pandas: runs every job in data/jobs.txt on pandas
itself and prints the transcript mini_pandas.kara must print. For each
job: `$ <job>`, then the result frame as `to_csv` writes it, or the error
pandas raised after `! `.

Needs pandas 3.0.5 on numpy, with neither bottleneck nor pyarrow installed
(both change which kernels and string arrays pandas uses).

Run: python3 -I -B oracle.py > expected.out"""
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


def read(path, kw):
    opts = {}
    if "sep" in kw:
        opts["sep"] = "\t" if kw["sep"] == "tab" else kw["sep"]
    if "na" in kw:
        opts["na_values"] = names(kw["na"])
    if kw.get("keep_default_na") == "0":
        opts["keep_default_na"] = False
    if kw.get("header") == "none":
        opts["header"] = None
    if "usecols" in kw:
        opts["usecols"] = names(kw["usecols"])
    if "dtype" in kw:
        opts["dtype"] = dict(p.split(":") for p in names(kw["dtype"]))
    return pd.read_csv(os.path.join("data", path), **opts)


def operand(df, tok):
    if tok.startswith("@"):
        return df[tok[1:]]
    return literal(tok)


OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
}
ARITH = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def side(df, tok):
    try:
        return literal_number(tok)
    except ValueError:
        return df[tok]


def literal_number(tok):
    try:
        return int(tok)
    except ValueError:
        return float(tok)


def isin_values(series, vals):
    if pd.api.types.is_numeric_dtype(series):
        return [literal_number(v) for v in vals]
    return vals


def step(df, op, toks):
    """One step of a job applied to the frame. Returns (frame, write_index)."""
    pos, kw = split_args(toks)
    if op == "dtypes":
        return pd.DataFrame({"column": list(df.columns), "dtype": [str(t) for t in df.dtypes]}), False
    if op == "head":
        return df.head(int(pos[0])), False
    if op == "tail":
        return df.tail(int(pos[0])), False
    if op == "select":
        return df[names(pos[0])], False
    if op == "drop":
        return df.drop(columns=names(pos[0])), False
    if op == "rename":
        return df.rename(columns=dict(p.split(":") for p in names(pos[0]))), False
    if op == "where":
        col, rel, rhs = toks
        return df[OPS[rel](df[col], operand(df, rhs))], False
    if op == "isna":
        return df[df[pos[0]].isna()], False
    if op == "notna":
        return df[df[pos[0]].notna()], False
    if op == "isin":
        s = df[pos[0]]
        return df[s.isin(isin_values(s, names(pos[1])))], False
    if op == "contains":
        case = kw.get("case", "1") == "1"
        return df[df[pos[0]].str.contains(pos[1], case=case, regex=False, na=False)], False
    if op == "startswith":
        return df[df[pos[0]].str.startswith(pos[1], na=False)], False
    if op == "between":
        return df[df[pos[0]].between(literal_number(pos[1]), literal_number(pos[2]))], False
    if op == "assign":
        new, eq, a, sym, b = toks
        assert eq == "="
        df = df.copy()
        df[new] = ARITH[sym](side(df, a), side(df, b))
        return df, False
    if op == "round":
        df = df.copy()
        df[pos[0]] = df[pos[0]].round(int(pos[1]))
        return df, False
    if op in ("upper", "lower", "strip"):
        df = df.copy()
        df[pos[0]] = getattr(df[pos[0]].str, op)()
        return df, False
    if op == "len":
        df = df.copy()
        df[pos[1]] = df[pos[0]].str.len()
        return df, False
    if op == "astype":
        df = df.copy()
        df[pos[0]] = df[pos[0]].astype({"int": "int64", "float": "float64", "str": "str"}[pos[1]])
        return df, False
    if op == "clip":
        df = df.copy()
        df[pos[0]] = df[pos[0]].clip(literal_number(pos[1]), literal_number(pos[2]))
        return df, False
    if op == "abs":
        df = df.copy()
        df[pos[0]] = df[pos[0]].abs()
        return df, False
    if op == "fillna":
        df = df.copy()
        df[pos[0]] = df[pos[0]].fillna(literal(pos[1]))
        return df, False
    if op in ("ffill", "bfill"):
        df = df.copy()
        df[pos[0]] = getattr(df[pos[0]], op)()
        return df, False
    if op == "dropna":
        return df.dropna(subset=names(kw["subset"]) if "subset" in kw else None, how=kw.get("how", "any")), False
    if op == "sort":
        by = names(pos[0])
        asc = [a == "1" for a in names(kw["asc"])] if "asc" in kw else True
        if isinstance(asc, list) and len(asc) == 1:
            asc = asc[0]
        return df.sort_values(by=by, ascending=asc, na_position=kw.get("na", "last"), kind="stable"), False
    if op == "dedup":
        keep = kw.get("keep", "first")
        return df.drop_duplicates(subset=names(kw["subset"]) if "subset" in kw else None,
                                  keep=False if keep == "false" else keep), False
    if op == "agg":
        keys = names(pos[0])
        spec = {}
        for p in names(pos[1]):
            c, f = p.split(":")
            spec[f"{c}_{f}"] = (c, f)
        return df.groupby(keys).agg(**spec).reset_index(), False
    if op == "size":
        return df.groupby(names(pos[0])).size().reset_index(name="size"), False
    if op == "transform":
        keys, col, func, new = pos
        df = df.copy()
        df[new] = df.groupby(names(keys))[col].transform(func)
        return df, False
    if op in ("gcumsum", "gdiff"):
        keys, col, new = pos
        df = df.copy()
        g = df.groupby(names(keys))[col]
        df[new] = g.cumsum() if op == "gcumsum" else g.diff()
        return df, False
    if op == "gshift":
        keys, col, n, new = pos
        df = df.copy()
        df[new] = df.groupby(names(keys))[col].shift(int(n))
        return df, False
    if op == "merge":
        right = read(pos[0], {})
        opts = {"how": kw.get("how", "inner")}
        if "on" in kw:
            opts["on"] = names(kw["on"])
        if "left_on" in kw:
            opts["left_on"] = names(kw["left_on"])
            opts["right_on"] = names(kw["right_on"])
        if "suffixes" in kw:
            a, b = kw["suffixes"].split(",")
            opts["suffixes"] = (a, b)
        return df.merge(right, **opts), False
    if op == "concat":
        return pd.concat([df, read(pos[0], {})], ignore_index=True), False
    if op == "pivot":
        opts = {"index": kw["index"], "columns": kw["columns"], "values": kw["values"], "aggfunc": kw["agg"]}
        if "fill" in kw:
            opts["fill_value"] = literal_number(kw["fill"])
        return df.pivot_table(**opts).reset_index(), False
    if op == "melt":
        opts = {"id_vars": names(kw["id"])}
        if "vars" in kw:
            opts["value_vars"] = names(kw["vars"])
        if "var" in kw:
            opts["var_name"] = kw["var"]
        if "value" in kw:
            opts["value_name"] = kw["value"]
        return df.melt(**opts), False
    if op == "crosstab":
        return pd.crosstab(df[pos[0]], df[pos[1]]).reset_index(), False
    if op == "rolling":
        col, w, func, new = pos
        df = df.copy()
        r = df[col].rolling(int(w), min_periods=int(kw["min"]) if "min" in kw else None)
        df[new] = getattr(r, func)()
        return df, False
    if op in ("cumsum", "cummax", "diff", "pct"):
        col, new = pos
        df = df.copy()
        df[new] = getattr(df[col], "pct_change" if op == "pct" else op)()
        return df, False
    if op == "shift":
        col, n, new = pos
        df = df.copy()
        df[new] = df[col].shift(int(n))
        return df, False
    if op == "rank":
        col, new = pos[0], pos[1]
        df = df.copy()
        df[new] = df[col].rank(method=kw.get("method", "average"), ascending="desc" not in pos)
        return df, False
    if op == "counts":
        return df[pos[0]].value_counts(normalize="norm" in pos).reset_index(), False
    if op == "describe":
        return df.describe(), True
    if op == "quantile":
        return df[names(pos[0])].quantile([float(q) for q in names(pos[1])]), True
    raise ValueError(f"unknown step {op}")


def run(line):
    steps = line.split(" | ")
    first = steps[0].split(" ")
    assert first[0] == "read"
    pos, kw = split_args(first[1:])
    df = read(pos[0], kw)
    with_index = False
    for s in steps[1:]:
        toks = s.split(" ")
        df, with_index = step(df, toks[0], toks[1:])
    return df.to_csv(index=with_index, lineterminator="\n")


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
