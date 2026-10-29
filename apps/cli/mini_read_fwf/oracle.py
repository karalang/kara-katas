"""The oracle: runs data/jobs.txt on pandas' read_fwf and prints what
mini_read_fwf.kara must print.

  read <file> [k=v ...]     pd.read_fwf(path, ...): the frame's shape, its
                            dtypes and to_csv (head=n prints the first n
                            rows only); with chunksize, each chunk

read takes colspecs (a:b,... with either end left out, or None), widths,
infer_nrows, header (n, a,b or None), names, usecols (positions or
names), index_col (n, a,b or a name), skiprows (n, a,b or [a,...]), skipfooter,
nrows, chunksize, comment, delimiter, thousands, decimal, encoding,
na_values (a,b or col:a|b,...), keep_default_na, na_filter,
skip_blank_lines, dtype (a type, or col:type,...) and dtype_backend.
`\\s` in a value is a space. An error prints as `! <exception>: <message>`.

Needs pandas 3.0.5.
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
warnings.simplefilter("ignore")


def ints(v):
    return [int(x) for x in v.split(",")] if "," in v else int(v)


def name_or_int(x):
    return int(x) if x.isdigit() else x


def bound(x):
    return None if x == "" else int(x)


def read_opts(opts):
    kw = {}
    head = None
    for o in opts:
        k, v = o.split("=", 1)
        v = v.replace("\\s", " ")
        if k == "colspecs":
            if v in ("None", "infer"):
                kw[k] = None if v == "None" else v
            else:
                kw[k] = [tuple(bound(x) for x in p.split(":")) for p in v.split(",")]
        elif k == "widths":
            kw[k] = [int(x) for x in v.split(",")]
        elif k in ("infer_nrows", "nrows", "chunksize", "skipfooter"):
            kw[k] = int(v)
        elif k == "header":
            kw[k] = None if v == "None" else ints(v)
        elif k == "names":
            kw[k] = v.split(",")
        elif k == "usecols":
            kw[k] = [name_or_int(x) for x in v.split(",")]
        elif k == "index_col":
            if "," in v:
                kw[k] = [name_or_int(x) for x in v.split(",")]
            else:
                kw[k] = name_or_int(v)
        elif k == "skiprows":
            if v.startswith("["):
                kw[k] = [int(x) for x in v[1:-1].split(",")]
            else:
                kw[k] = [int(x) for x in v.split(",")] if "," in v else int(v)
        elif k == "dtype":
            if ":" in v:
                kw[k] = dict(p.split(":", 1) for p in v.split(","))
            else:
                kw[k] = v
        elif k == "na_values":
            if ":" in v:
                kw[k] = {c: x.split("|") for c, x in (p.split(":", 1) for p in v.split(","))}
            else:
                kw[k] = v.split(",")
        elif k in ("keep_default_na", "na_filter", "skip_blank_lines"):
            kw[k] = v == "True"
        elif k == "head":
            head = int(v)
        else:
            kw[k] = v
    return kw, head


def frame(df, head):
    print(f"shape {df.shape}")
    for c, t in df.dtypes.items():
        print(f"  {c!r}: {t}")
    if head is not None:
        df = df.head(head)
    sys.stdout.write(df.to_csv(lineterminator="\n"))


def run(job):
    w = job.split(" ")
    path = os.path.join("data", w[1])
    try:
        kw, head = read_opts(w[2:])
        if "chunksize" in kw:
            with pd.read_fwf(path, **kw) as reader:
                for k, df in enumerate(reader):
                    print(f"chunk {k}")
                    frame(df, head)
            print("done")
        else:
            frame(pd.read_fwf(path, **kw), head)
    except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
        print(f"! {type(e).__name__}: {e}")


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line:
            print(f"$ {line}")
            run(line)
