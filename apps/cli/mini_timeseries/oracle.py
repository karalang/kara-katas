"""The oracle for mini_timeseries: runs every job in data/jobs.txt on
pandas itself and prints the transcript mini_timeseries.kara must print.
For each job: `$ <job>`, then the result frame as `to_csv(index=False)`
writes it, or the error pandas raised after `! `. In a job, `_` stands
for a space inside a quoted value, a format and a `format=` option.

Needs pandas 3.0.5 on numpy, with neither bottleneck nor pyarrow
installed (both change which kernels and string arrays pandas uses).

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
        return tok[1:-1].replace("_", " ")
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


def split_args(toks):
    pos, kw = [], {}
    for t in toks:
        if "=" in t and not t.startswith("=") and t != "==" and t not in ("<=", ">=", "!="):
            k, v = t.split("=", 1)
            kw[k] = v
        else:
            pos.append(t)
    return pos, kw


def names(s):
    return s.split(",") if s else []


def read(path, pos, kw):
    df = pd.read_csv(os.path.join("data", path))
    for c in names(kw.get("dates", "")):
        opts = {}
        if "format" in kw:
            opts["format"] = kw["format"].replace("_", " ")
        if "unit" in kw:
            opts["unit"] = kw["unit"]
        if "coerce" in pos:
            opts["errors"] = "coerce"
        df[c] = pd.to_datetime(df[c], **opts)
    return df


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


def operand(df, tok):
    if tok.startswith("@"):
        return df[tok[1:]]
    return literal(tok)


def side(df, tok):
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        return df[tok]


def part(s, name):
    if name == "week":
        return s.dt.isocalendar().week
    if name in ("day_name", "month_name"):
        return getattr(s.dt, name)()
    return getattr(s.dt, name)


def named(specs):
    spec = {}
    for p in names(specs):
        c, f = p.split(":")
        spec[f"{c}_{f}"] = (c, f)
    return spec


def step(df, op, toks):
    pos, kw = split_args(toks)
    if op == "dtypes":
        return pd.DataFrame({"column": list(df.columns), "dtype": [str(t) for t in df.dtypes]})
    if op == "head":
        return df.head(int(pos[0]))
    if op == "tail":
        return df.tail(int(pos[0]))
    if op == "select":
        return df[names(pos[0])]
    if op == "where":
        col, rel, rhs = toks
        return df[OPS[rel](df[col], operand(df, rhs))]
    if op == "isna":
        return df[df[pos[0]].isna()]
    if op == "assign":
        new, eq, a, sym, b = toks
        df = df.copy()
        df[new] = ARITH[sym](side(df, a), side(df, b))
        return df
    if op == "round":
        df = df.copy()
        df[pos[0]] = df[pos[0]].round(int(pos[1]))
        return df
    if op == "sort":
        by = names(pos[0])
        asc = [a == "1" for a in names(kw["asc"])] if "asc" in kw else True
        if isinstance(asc, list) and len(asc) == 1:
            asc = asc[0]
        return df.sort_values(by=by, ascending=asc, kind="stable")
    if op == "agg":
        return df.groupby(names(pos[0])).agg(**named(pos[1])).reset_index()
    if op == "dt":
        col, name, new = pos
        df = df.copy()
        df[new] = part(df[col], name)
        return df
    if op in ("floor", "ceil"):
        col, freq, new = pos
        df = df.copy()
        df[new] = getattr(df[col].dt, op)(freq)
        return df
    if op == "dtround":
        col, freq, new = pos
        df = df.copy()
        df[new] = df[col].dt.round(freq)
        return df
    if op == "strftime":
        col, fmt, new = pos
        df = df.copy()
        df[new] = df[col].dt.strftime(fmt.replace("_", " "))
        return df
    if op == "normalize":
        col, new = pos
        df = df.copy()
        df[new] = df[col].dt.normalize()
        return df
    if op == "between_time":
        col, a, b = pos
        idx = pd.DatetimeIndex(df[col])
        return df.iloc[idx.indexer_between_time(a, b)]
    if op == "sub":
        a, b, new = pos
        df = df.copy()
        df[new] = df[a] - df[b]
        return df
    if op == "tdiff":
        col, new = pos
        df = df.copy()
        df[new] = df[col].diff()
        return df
    if op == "secs":
        col, new = pos
        df = df.copy()
        df[new] = df[col].dt.total_seconds()
        return df
    if op == "resample":
        col, freq, specs = pos
        opts = {"on": col}
        for k in ("closed", "label", "origin", "offset"):
            if k in kw:
                opts[k] = kw[k]
        if "by" in kw:
            r = df.groupby(names(kw["by"])).resample(freq, **opts)
        else:
            r = df.resample(freq, **opts)
        return r.agg(**named(specs)).reset_index()
    if op == "ohlc":
        col, freq, val = pos
        return df.resample(freq, on=col)[val].ohlc().reset_index()
    if op == "asfreq":
        col, freq = pos[0], pos[1]
        method = pos[2] if len(pos) > 2 else None
        return df.set_index(col).asfreq(freq, method=method).reset_index()
    if op == "trolling":
        col, win, val, func, new = pos
        df = df.copy()
        df[new] = getattr(df.rolling(win, on=col)[val], func)()
        return df
    if op == "tz":
        col, how, zone = pos
        df = df.copy()
        df[col] = df[col].dt.tz_localize(zone) if how == "localize" else df[col].dt.tz_convert(zone)
        return df
    raise ValueError(f"unknown step {op}")


def first_frame(toks):
    pos, kw = split_args(toks[1:])
    if toks[0] == "range":
        start, end, freq = pos
        return pd.DataFrame({"t": pd.date_range(start, end, freq=freq, tz=kw.get("tz"))})
    return read(pos[0], pos[1:], kw)


def run(line):
    steps = line.split(" | ")
    df = first_frame(steps[0].split(" "))
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
