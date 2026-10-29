"""The oracle: runs data/jobs.txt on pandas' read_csv with
engine="python" and prints what mini_read_table.kara must print.

  read <file> [k=v ...]     pd.read_csv(path, engine="python", ...) (or
                            pd.read_table with fn=table): the warnings,
                            then the frame's shape, its dtypes and to_csv
                            (head=n prints the first n rows only); with
                            chunksize, each chunk

read takes sep, delimiter, dialect, quotechar, escapechar, doublequote,
skipinitialspace, quoting, header (n, a,b or None), names, usecols
(positions or names), index_col (n, a,b, a name or False), skiprows (n,
a,b or [a,...]), skipfooter, nrows, chunksize, comment, thousands,
decimal, true_values, false_values, encoding, encoding_errors,
on_bad_lines, na_values (a,b), keep_default_na, na_filter,
skip_blank_lines, dtype (a type, or col:type,...) and dtype_backend.
{sp} in a value is a space and {tab} a tab. A warning prints as
`warn: <message>`, an error as `! <exception>: <message>`.

Needs pandas 3.0.5.
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def ints(v):
    return [int(x) for x in v.split(",")] if "," in v else int(v)


def name_or_int(x):
    return int(x) if x.isdigit() else x


def read_opts(opts):
    kw = {}
    head = None
    fn = pd.read_csv
    for o in opts:
        k, v = o.split("=", 1)
        v = v.replace("{sp}", " ").replace("{tab}", "\t")
        if k in ("nrows", "chunksize", "skipfooter", "quoting"):
            kw[k] = int(v)
        elif k in ("sep", "delimiter"):
            kw[k] = None if v == "None" else v
        elif k == "header":
            kw[k] = None if v == "None" else ints(v)
        elif k in ("names", "true_values", "false_values", "na_values"):
            kw[k] = v.split(",")
        elif k == "usecols":
            kw[k] = [name_or_int(x) for x in v.split(",")]
        elif k == "index_col":
            if v in ("False", "True"):
                kw[k] = v == "True"
            elif "," in v:
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
        elif k in ("keep_default_na", "na_filter", "skip_blank_lines",
                   "doublequote", "skipinitialspace"):
            kw[k] = v == "True"
        elif k == "head":
            head = int(v)
        elif k == "fn":
            fn = pd.read_table
        else:
            kw[k] = v
    return fn, kw, head


def frame(df, head):
    print(f"shape {df.shape}")
    for c, t in df.dtypes.items():
        print(f"  {c!r}: {t}")
    if head is not None:
        df = df.head(head)
    sys.stdout.write(df.to_csv(lineterminator="\n"))


def warned(w):
    for x in w:
        msg = str(x.message).rstrip("\n")
        print(f"warn: {msg}")
    w.clear()


def run(job):
    w = job.split(" ")
    path = os.path.join("data", w[1])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            fn, kw, head = read_opts(w[2:])
            kw["engine"] = "python"
            if "chunksize" in kw:
                with fn(path, **kw) as reader:
                    for k, df in enumerate(reader):
                        warned(caught)
                        print(f"chunk {k}")
                        frame(df, head)
                print("done")
            else:
                df = fn(path, **kw)
                warned(caught)
                frame(df, head)
        except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
            warned(caught)
            print(f"! {type(e).__name__}: {e}")


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line:
            print(f"$ {line}")
            run(line)
