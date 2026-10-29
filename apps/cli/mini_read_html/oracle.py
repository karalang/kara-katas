"""The oracle: runs data/jobs.txt on pandas' read_html and prints what
mini_read_html.kara must print.

  read <file> [k=v ...]     pd.read_html(path, ...): the number of tables,
                            then for each one its shape, the dtypes and
                            to_csv (head=n prints the first n rows only)

read takes match, attrs (k:v,...), header (n, a,b or None), index_col
(n or a,b), skiprows (n, a,b or start:stop:step), thousands (None for
none), decimal, na_values (a,b,...), keep_default_na, displayed_only,
extract_links, encoding, flavor (lxml unless given) and dtype_backend. `\\s` in a value is a
space. An error prints as `! <exception>: <message>`.

Needs pandas 3.0.5 with lxml 6.1 (libxml2 2.14).
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


def read_opts(opts):
    kw = {}
    head = None
    for o in opts:
        k, v = o.split("=", 1)
        v = v.replace("\\s", " ")
        if k == "attrs":
            kw[k] = dict(p.split(":", 1) for p in v.split(","))
        elif k in ("header", "index_col"):
            kw[k] = None if v == "None" else ints(v)
        elif k == "skiprows":
            if ":" in v:
                a, b, c = v.split(":")
                kw[k] = slice(int(a), int(b), int(c))
            else:
                kw[k] = ints(v)
        elif k == "thousands":
            kw[k] = None if v == "None" else v
        elif k == "na_values":
            kw[k] = v.split(",")
        elif k in ("keep_default_na", "displayed_only"):
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
        # Only lxml: html5lib is not installed, and pandas' default flavor
        # would fall back to it when lxml finds no table.
        kw.setdefault("flavor", "lxml")
        tables = pd.read_html(path, **kw)
        print(f"tables {len(tables)}")
        for k, df in enumerate(tables):
            print(f"table {k}")
            frame(df, head)
    except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
        print(f"! {type(e).__name__}: {e}")


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line:
            print(f"$ {line}")
            run(line)
