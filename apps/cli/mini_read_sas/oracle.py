"""The oracle: runs data/jobs.txt on pandas' SAS readers and prints what
mini_read_sas.kara must print.

  meta <file>                 the reader's view of the file: for a
                              sas7bdat file its layout, encoding, dates,
                              counts, compression and every column; for an
                              xport file its file and member headers and
                              every field
  read <file> [k=v ...]       read_sas(file, ...): the shape, the index
                              if one was set, the dtypes, then to_csv
  chunks <file> <n> [k=v ...] read_sas(file, chunksize=n, ...), each chunk
                              as read prints it
  rows <file> <n,n,..> [k=v]  read_sas(file, iterator=True, ...), then
                              reader.read(n) for each n
  reader <file> [k=v ...]     SAS7BDATReader(file, ...).read(), for the
                              options read_sas does not pass on

The options are format, index and encoding (text), and convert_dates,
blank_missing, convert_text and convert_header_text (True or False).

Needs pandas 3.0.5.
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd
from pandas.io.sas.sas7bdat import SAS7BDATReader

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
warnings.simplefilter("ignore")


def options(words):
    kw = {}
    for w in words:
        k, v = w.split("=", 1)
        kw[k] = (v == "True") if v in ("True", "False") else v
    return kw


def show(df):
    print(f"shape: {df.shape[0]} x {df.shape[1]}")
    if df.index.name is not None:
        print(f"index: {df.index.name!r} {df.index.dtype}")
    for c in df.columns:
        print(f"  {c!r}: {df[c].dtype}")
    sys.stdout.write(df.to_csv())


def meta(path):
    r = pd.read_sas(path, iterator=True)
    with r:
        if isinstance(r, SAS7BDATReader):
            print(f"sas7bdat: U64={r.U64} byte_order={r.byte_order!r} "
                  f"encoding={r.inferred_encoding!r}")
            print(f"created {r.date_created} modified {r.date_modified}")
            print(f"header {r.header_length}, page {r._page_length}, "
                  f"{r.row_count} rows of {r.row_length} bytes, {r.column_count} columns")
            print(f"compression {r.compression!r}, "
                  f"creator_proc {getattr(r, 'creator_proc', None)!r}")
            offsets = r.column_data_offsets()
            for c in r.columns:
                print(f"  {c.col_id} {c.name!r}: {c.ctype.decode()} length={c.length} "
                      f"offset={offsets[c.col_id]} format={c.format!r} label={c.label!r}")
        else:
            print(f"xport: {r.file_info}")
            print(f"member: {r.member_info}")
            for f in r.fields:
                print(f"  {f['name']!r}: {f['ntype']} length={f['field_length']} "
                      f"format={f['nform']!r} {f['nfl']}.{f['num_decimals']} "
                      f"position={f['npos']} label={f['label']!r}")
            print(f"{r.nobs} obs of {r.record_length} bytes")


def job(line):
    w = line.split()
    path = os.path.join("data", w[1])
    if w[0] == "meta":
        meta(path)
    elif w[0] == "read":
        show(pd.read_sas(path, **options(w[2:])))
    elif w[0] == "reader":
        with SAS7BDATReader(path, **options(w[2:])) as r:
            show(r.read())
    elif w[0] == "chunks":
        with pd.read_sas(path, chunksize=int(w[2]), **options(w[3:])) as it:
            for chunk in it:
                print("-- chunk")
                show(chunk)
    elif w[0] == "rows":
        with pd.read_sas(path, iterator=True, **options(w[3:])) as r:
            for n in w[2].split(","):
                print(f"-- read({n})")
                show(r.read(int(n)))


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
            print(f"! {type(e).__name__}: {e}")
