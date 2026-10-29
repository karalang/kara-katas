"""The oracle for mini_pandas_clean: runs every job in data/jobs.txt on
pandas itself and prints the transcript mini_pandas_clean.kara must
print. For each job: `$ <job>`, then the result frame as
`to_csv(index=False)` writes it (or as `to_json` writes it, after a
`json` step), or the error pandas raised after `! `.

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
    """A text argument: \\s is a space and \\e the empty string."""
    return "" if tok == "\\e" else tok.replace("\\s", " ")


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
    opts = {}
    if "dtype" in kw:
        opts["dtype"] = dict(p.split(":") for p in names(kw["dtype"]))
    return pd.read_csv(os.path.join("data", path), **opts)


OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
}


def str_op(s, op, args, kw):
    """One Series.str method."""
    if op in ("lower", "upper", "strip", "title", "capitalize", "swapcase", "len"):
        return getattr(s.str, op)()
    if op == "zfill":
        return s.str.zfill(int(args[0]))
    if op == "pad":
        return s.str.pad(int(args[0]), side=kw.get("side", "left"), fillchar=kw.get("fill", " "))
    if op == "slice":
        return s.str.slice(int(args[0]), int(args[1]) if len(args) > 1 else None)
    if op == "replace":
        return s.str.replace(text(args[0]), text(args[1]), regex=False)
    if op in ("removeprefix", "removesuffix", "find", "count"):
        return getattr(s.str, op)(text(args[0]))
    raise ValueError(f"unknown str method {op}")


def ewm_args(kw):
    out = {}
    for k in ("com", "span", "halflife", "alpha"):
        if k in kw:
            out[k] = float(kw[k])
    out["adjust"] = kw.get("adjust", "1") == "1"
    out["ignore_na"] = kw.get("ignore_na", "0") == "1"
    out["min_periods"] = int(kw.get("minp", "0"))
    return out


def ewm_of(s, func, kw):
    e = s.ewm(**ewm_args(kw))
    if func == "mean":
        return e.mean()
    return getattr(e, func)(bias=kw.get("bias", "0") == "1")


def step(df, op, toks):
    """One step of a job applied to the frame. Returns (frame, json_args)."""
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
        return df[OPS[rel](df[col], literal(rhs))]
    if op == "agg":
        keys = names(pos[0])
        spec = {}
        for p in names(pos[1]):
            c, f = p.split(":")
            spec[f"{c}_{f}"] = (c, f)
        return df.groupby(keys).agg(**spec).reset_index()
    df = df.copy()
    if op == "str":
        col = pos[0]
        df[kw.get("as", col)] = str_op(df[col], pos[1], pos[2:], kw)
        return df
    if op == "cat":
        a, b = pos[0], pos[1]
        df[kw["as"]] = df[a].str.cat(df[b], sep=text(kw.get("sep", "\\e")), na_rep=kw.get("na"))
        return df
    if op == "numeric":
        col = pos[0]
        df[kw.get("as", col)] = pd.to_numeric(df[col], errors="coerce" if "coerce" in pos else "raise")
        return df
    if op == "duplicated":
        keep = kw.get("keep", "first")
        df[kw["as"]] = df.duplicated(subset=names(kw["subset"]) if "subset" in kw else None,
                                     keep=False if keep == "false" else keep)
        return df
    if op in ("mask", "keep"):
        col, rel, rhs = pos[0], pos[1], pos[2]
        cond = OPS[rel](df[col], literal(rhs))
        method = df[col].mask if op == "mask" else df[col].where
        df[col] = method(cond, literal(kw["other"])) if "other" in kw else method(cond)
        return df
    if op in ("combine", "update"):
        on = kw["on"]
        other = read(pos[0], {}).set_index(on)
        mine = df.set_index(on)
        if op == "combine":
            return mine.combine_first(other).reset_index()
        mine.update(other)
        return mine.reset_index()
    if op == "asof":
        opts = {"on": kw["on"]}
        if "by" in kw:
            opts["by"] = kw["by"]
        if "direction" in kw:
            opts["direction"] = kw["direction"]
        if "tolerance" in kw:
            opts["tolerance"] = int(kw["tolerance"])
        if kw.get("exact") == "0":
            opts["allow_exact_matches"] = False
        return pd.merge_asof(df, read(pos[0], {}), **opts)
    if op == "ewm":
        col, func = pos[0], pos[1]
        if "by" in kw:
            df[kw["as"]] = df.groupby(kw["by"])[col].transform(lambda s: ewm_of(s, func, kw))
        else:
            df[kw["as"]] = ewm_of(df[col], func, kw)
        return df
    raise ValueError(f"unknown step {op}")


def to_json(df, toks):
    pos, kw = split_args(toks)
    lines = kw.get("lines") == "1"
    out = df.reset_index(drop=True).to_json(
        orient=pos[0],
        double_precision=int(kw.get("precision", "10")),
        force_ascii=kw.get("ascii", "1") == "1",
        lines=lines,
    )
    return out if lines else out + "\n"


def run(line):
    steps = line.split(" | ")
    first = steps[0].split(" ")
    assert first[0] == "read"
    pos, kw = split_args(first[1:])
    df = read(pos[0], kw)
    for s in steps[1:]:
        toks = s.split(" ")
        if toks[0] == "json":
            return to_json(df, toks[1:])
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
