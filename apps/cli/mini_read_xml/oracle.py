"""The oracle: runs data/jobs.txt on pandas' read_xml and to_xml and
prints what mini_read_xml.kara must print.

  read <file> [k=v ...]               pd.read_xml(path, ...): the shape,
                                      the dtypes, then to_csv (head=n
                                      prints the first n rows only)
  write <file> [k=v ...] | [k=v ...]  read_xml with the options before the
                                      bar, then df.to_xml(...) with the
                                      options after it, printed as returned

read takes xpath, namespaces (p=uri;p=uri), elems_only, attrs_only,
names, dtype (col:type,...), parse_dates (cols), encoding, parser,
iterparse (row:col,col,...) and compression; to_xml takes parser, index,
root_name, row_name, na_rep, attr_cols, elem_cols, namespaces, prefix,
encoding, xml_declaration and pretty_print. An error prints as
`! <exception>: <message>`.

Needs pandas 3.0.5 with lxml 6.1 (libxml2 2.14).
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
warnings.simplefilter("ignore")


def namespaces(v):
    out = {}
    for part in v.split(";"):
        p, uri = part.split("=", 1)
        out[p] = uri
    return out


def read_opts(opts):
    kw = {}
    head = None
    for o in opts:
        k, v = o.split("=", 1)
        if k == "namespaces":
            kw[k] = namespaces(v)
        elif k in ("elems_only", "attrs_only"):
            kw[k] = v == "True"
        elif k in ("names", "parse_dates"):
            kw[k] = v.split(",")
        elif k == "dtype":
            kw[k] = dict(x.split(":") for x in v.split(","))
        elif k == "iterparse":
            row, _, cols = v.partition(":")
            kw[k] = {row: cols.split(",") if cols else []}
        elif k == "head":
            head = int(v)
        else:
            kw[k] = v
    return kw, head


def write_opts(opts):
    kw = {}
    for o in opts:
        k, v = o.split("=", 1)
        if k == "namespaces":
            kw[k] = namespaces(v)
        elif k in ("index", "xml_declaration", "pretty_print"):
            kw[k] = v == "True"
        elif k in ("attr_cols", "elem_cols"):
            kw[k] = v.split(",")
        else:
            kw[k] = v
    return kw


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
        if w[0] == "read":
            kw, head = read_opts(w[2:])
            frame(pd.read_xml(path, **kw), head)
        elif w[0] == "write":
            bar = w.index("|")
            kw, _ = read_opts(w[2:bar])
            df = pd.read_xml(path, **kw)
            out = df.to_xml(**write_opts(w[bar + 1:]))
            sys.stdout.write(out + "\n")
    except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
        print(f"! {type(e).__name__}: {e}")


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line:
            print(f"$ {line}")
            run(line)
