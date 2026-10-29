"""The oracle: runs data/jobs.txt on openpyxl and pandas and prints what
mini_read_excel.kara must print.

  sheets <file>                    load_workbook(read_only=True, data_only=True,
                                   keep_links=False), as pandas opens it: the
                                   sheet names, the epoch, and each sheet's
                                   state and dimension
  rows <file> <sheet> [opts]       ws.iter_rows(..., values_only=True), one
                                   repr(tuple) per row
  cells <file> <sheet> [opts]      the same without values_only: each cell's
                                   coordinate, data_type, number_format,
                                   is_date and repr(value)
  read <file> [k=v ...]            pandas.read_excel(engine="openpyxl", ...):
                                   the shape, the dtypes, then to_csv

rows and cells take min_row=, max_row=, min_col=, max_col=, "formulas"
(data_only=False) and "reset" (reset_dimensions() first). In a job, \\s
is a space.

Needs openpyxl 3.1.5 (with lxml) and pandas 3.0.5.
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import openpyxl
import pandas as pd
from openpyxl.cell.read_only import EmptyCell

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
warnings.simplefilter("ignore")


def text(s):
    return s.replace("\\s", " ")


def fail(e):
    msg = str(e)
    print(f"! {type(e).__name__}: {msg}")


def sheets(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True, keep_links=False)
    print("sheets", repr(wb.sheetnames))
    print("epoch", wb.epoch.date().isoformat())
    for ws in wb.worksheets:
        try:
            dim = ws.calculate_dimension()
        except ValueError as e:
            dim = f"! {e}"
        print(f"{ws.title!r} {ws.sheet_state} rows {ws.min_row}..{ws.max_row} cols {ws.min_column}..{ws.max_column} {dim}")


def rows(path, name, opts, values_only):
    formulas = "formulas" in opts
    wb = openpyxl.load_workbook(path, read_only=True, data_only=not formulas, keep_links=False)
    ws = wb[name]
    if "reset" in opts:
        ws.reset_dimensions()
    kw = {k: int(v) for k, v in (o.split("=") for o in opts if "=" in o)}
    n = 0
    for row in ws.iter_rows(values_only=values_only, **kw):
        n += 1
        if values_only:
            print(repr(row))
        else:
            out = []
            for c in row:
                if isinstance(c, EmptyCell):
                    out.append("-")
                else:
                    out.append(f"{c.coordinate} {c.data_type} {c.number_format!r} {c.is_date} {c.value!r}")
            print(" | ".join(out) if out else "()")
    print(f"({n} rows)")


def listy(v, conv=str):
    return [conv(x) for x in v.split(",")]


def maybe_int(x):
    return int(x) if x.lstrip("-").isdigit() else x


def read(path, opts):
    kw = {}
    for o in opts:
        k, v = o.split("=", 1)
        v = text(v)
        if k == "sheet_name":
            kw[k] = None if v == "None" else (listy(v, maybe_int) if "," in v else maybe_int(v))
        elif k in ("header", "index_col"):
            kw[k] = None if v == "None" else maybe_int(v)
        elif k in ("nrows", "skipfooter"):
            kw[k] = int(v)
        elif k == "skiprows":
            kw[k] = listy(v, int) if "," in v else int(v)
        elif k == "usecols":
            if ":" in v or (v.replace(",", "").isalpha() and v.replace(",", "").isupper() and all(len(x) <= 2 for x in v.split(","))):
                kw[k] = v
            elif v.replace(",", "").isdigit():
                kw[k] = listy(v, int)
            else:
                kw[k] = listy(v)
        elif k in ("names", "na_values", "true_values", "false_values"):
            kw[k] = listy(v)
        elif k == "dtype":
            kw[k] = dict(x.split(":") for x in v.split(","))
        elif k in ("keep_default_na", "parse_dates"):
            kw[k] = v == "True"
    got = pd.read_excel(path, engine="openpyxl", **kw)
    if isinstance(got, dict):
        for name, df in got.items():
            print(f"[{name!r}]")
            frame(df, "index_col" in kw)
    else:
        frame(got, "index_col" in kw)


def frame(df, with_index):
    print(f"shape {df.shape}")
    if with_index:
        print(f"  index {df.index.name!r}: {df.index.dtype}")
    for c, t in df.dtypes.items():
        print(f"  {c!r}: {t}")
    sys.stdout.write(df.to_csv(index=with_index, lineterminator="\n"))


def run(job):
    w = job.split(" ")
    path = os.path.join("data", w[1])
    try:
        if w[0] == "sheets":
            sheets(path)
        elif w[0] == "rows":
            rows(path, text(w[2]), w[3:], True)
        elif w[0] == "cells":
            rows(path, text(w[2]), w[3:], False)
        elif w[0] == "read":
            read(path, w[2:])
    except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
        fail(e)


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line:
            print(f"$ {line}")
            run(line)
