"""The oracle: runs data/jobs.txt on pandas' SQL reader and writer over
Python's sqlite3, and prints what mini_read_sql.kara must print.

  read <db> [k=v ...] :: <sql>          pd.read_sql_query(sql, con, ...):
                                        the shape, the index, the dtypes,
                                        then to_csv (head=n prints the
                                        first n rows only)
  chunks <db> chunksize=n [k=v ...] :: <sql>
                                        the same with chunksize, one frame
                                        per chunk
  schema <db> name=t [keys=a,b] [k=v ...] :: <sql>
                                        pd.io.sql.get_schema of the frame
  tosql <db> name=t [k=v ...] :: <sql> ;; <sql> ...
                                        reads the first query, writes the
                                        frame back with df.to_sql(...) into
                                        a copy of the database held in
                                        memory, prints the row count, then
                                        reads each later query from it

read takes index_col (a,b), params (a list: 'text', 12, 1.5, None),
named (k=value,...), parse_dates (col or col:format-or-unit, ...),
dtype (type, or col:type,...), dtype_backend and head; to_sql takes
name, if_exists, index, index_label and sqltype (col:type,...), and
get_schema name, keys and sqltype. `\\s` in a value is a space. An error
prints as `! <exception>: <message>`.

Needs pandas 3.0.5 and SQLite 3.45 (Python 3.13's sqlite3).
Run: python3 -I -B oracle.py > expected.out"""
import os
import sqlite3
import sys
import warnings

import pandas as pd
from pandas.io.sql import get_schema

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
warnings.simplefilter("ignore")


def split_top(v, sep):
    out, cur, q = [], "", False
    for ch in v:
        if ch == "'":
            q = not q
        if ch == sep and not q:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def literal(t):
    if t == "None":
        return None
    if t.startswith("'"):
        return t[1:-1].replace("''", "'")
    if t.startswith("x'"):
        return bytes.fromhex(t[2:-1])
    try:
        return int(t)
    except ValueError:
        return float(t)


def opts_of(words):
    kw, head, out = {}, None, {}
    for o in words:
        k, v = o.split("=", 1)
        v = v.replace("\\s", " ")
        if k == "index_col":
            kw[k] = v.split(",") if "," in v else v
        elif k == "params":
            kw[k] = [literal(t) for t in split_top(v, ",")]
        elif k == "named":
            kw["params"] = {a: literal(b) for a, b in (p.split("=", 1) for p in split_top(v, ","))}
        elif k == "parse_dates":
            parts = v.split(",")
            if any(":" in p for p in parts):
                kw[k] = {}
                for p in parts:
                    c, _, f = p.partition(":")
                    kw[k][c] = f or None
            else:
                kw[k] = parts
        elif k == "dtype":
            kw[k] = dict(p.split(":", 1) for p in v.split(",")) if ":" in v else v
        elif k == "chunksize":
            kw[k] = int(v)
        elif k == "head":
            head = int(v)
        elif k in ("dtype_backend", "coerce_float"):
            kw[k] = v if k == "dtype_backend" else v == "True"
        elif k == "keys":
            out[k] = v.split(",") if "," in v else v
        elif k == "index":
            out[k] = v == "True"
        elif k == "sqltype":
            out["dtype"] = dict(p.split(":", 1) for p in v.split(","))
        else:
            out[k] = v
    return kw, head, out


def frame(df, head):
    print(f"shape {df.shape}")
    if not isinstance(df.index, pd.RangeIndex):
        for name, t in zip(df.index.names, [df.index.get_level_values(i).dtype for i in range(df.index.nlevels)]):
            print(f"  index {name!r}: {t}")
    for c, t in df.dtypes.items():
        print(f"  {c!r}: {t}")
    if head is not None:
        df = df.head(head)
    sys.stdout.write(df.to_csv(lineterminator="\n"))


def connect(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def run(job):
    head_part, _, sql_part = job.partition(" :: ")
    w = head_part.split(" ")
    kind, path = w[0], os.path.join("data", w[1])
    sqls = sql_part.split(" ;; ")
    kw, head, out = opts_of(w[2:])
    try:
        con = connect(path)
        if kind == "read":
            frame(pd.read_sql_query(sqls[0], con, **kw), head)
        elif kind == "chunks":
            for k, df in enumerate(pd.read_sql_query(sqls[0], con, **kw)):
                print(f"chunk {k}")
                frame(df, head)
        elif kind == "schema":
            df = pd.read_sql_query(sqls[0], con, **kw)
            print(get_schema(df, out["name"], keys=out.get("keys"), dtype=out.get("dtype")))
        elif kind == "tosql":
            mem = sqlite3.connect(":memory:")
            con.backup(mem)
            df = pd.read_sql_query(sqls[0], mem, **kw)
            name = out.pop("name")
            print(f"to_sql {df.to_sql(name, mem, **out)}")
            for q in sqls[1:]:
                print(f"> {q}")
                frame(pd.read_sql_query(q, mem), None)
    except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
        print(f"! {type(e).__name__}: {e}")


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line and not line.startswith("#"):
            print(f"$ {line}")
            run(line)
