"""The oracle: runs data/jobs.txt on pandas' Stata reader and prints what
mini_read_stata.kara must print.

  meta <file>                  StataReader(file): the format, byte order,
                               counts, data label and time stamp, each
                               variable's name, type, format, value label
                               name and label, then the value label tables
  read <file> [k=v ...]        read_stata(file, ...): the shape, the dtypes
                               (with a categorical's categories), then to_csv
  chunks <file> <n> [k=v ...]  read_stata(file, chunksize=n, ...), each chunk
                               as read prints it

The options are convert_dates, convert_categoricals, convert_missing,
preserve_dtypes and order_categoricals (True or False), index_col (a
name) and columns (names, comma-separated).

Needs pandas 3.0.5.
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
warnings.simplefilter("ignore")


def fail(e):
    print(f"! {type(e).__name__}: {e}")


def py(x):
    if isinstance(x, np.generic):
        x = x.item()
    return repr(x)


def options(words):
    kw = {}
    for w in words:
        k, v = w.split("=", 1)
        if k == "columns":
            kw[k] = v.split(",")
        elif k == "index_col":
            kw[k] = v
        else:
            kw[k] = v == "True"
    return kw


def show(df):
    print(f"shape: {df.shape[0]} x {df.shape[1]}")
    if df.index.name is not None:
        print(f"index: {df.index.name!r} {df.index.dtype}")
    for c in df.columns:
        dt = df[c].dtype
        if isinstance(dt, pd.CategoricalDtype):
            cats = ", ".join(py(x) for x in dt.categories)
            print(f"  {c!r}: category [{cats}] ordered={dt.ordered}")
        else:
            print(f"  {c!r}: {dt}")
    sys.stdout.write(df.to_csv())


def meta(path):
    with pd.io.stata.StataReader(path) as r:
        r._ensure_open()
        print(f"format {r._format_version}, byteorder {r._byteorder!r}, "
              f"{r._nobs} obs, {r._nvar} vars")
        print(f"data_label: {r.data_label!r}")
        print(f"time_stamp: {r.time_stamp!r}")
        labels = r.variable_labels()
        for i, name in enumerate(r._varlist):
            print(f"  {name!r}: type={r._typlist[i]!r} fmt={r._fmtlist[i]!r} "
                  f"lbl={r._lbllist[i]!r} label={labels[name]!r}")
        for name, table in r.value_labels().items():
            pairs = ", ".join(f"{int(k)}: {v!r}" for k, v in table.items())
            print(f"  value labels {name!r}: {{{pairs}}}")


def job(line):
    w = line.split()
    path = os.path.join("data", w[1])
    if w[0] == "meta":
        meta(path)
    elif w[0] == "read":
        show(pd.read_stata(path, **options(w[2:])))
    elif w[0] == "chunks":
        with pd.read_stata(path, chunksize=int(w[2]), **options(w[3:])) as it:
            for chunk in it:
                print("-- chunk")
                show(chunk)


with open("data/jobs.txt", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line:
            continue
        print(f"$ {line}")
        sys.stdout.flush()
        try:
            job(line)
        except Exception as e:
            fail(e)
