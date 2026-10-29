"""The oracle: runs data/jobs.txt on pandas' read_json and prints what
mini_read_json.kara must print.

  read <file> [k=v ...]     pd.read_json(path, ...): the warnings, then
                            the frame's (or Series') shape, its dtypes
                            and to_csv (head=n prints the first n rows
                            only); with chunksize, each chunk

read takes orient, typ, dtype (True, False, a type, or col:type,...),
convert_axes, convert_dates (True, False or a,b), keep_default_dates,
precise_float, date_unit, encoding, encoding_errors, lines, chunksize,
nrows, dtype_backend and engine. A warning prints as `warn: <message>`,
an error as `! <exception>: <message>`. A carriage return inside a
value prints as \\r: kara's checkout turns a raw CR in expected.out
into LF.

Needs pandas 3.0.5.
Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
import warnings

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def flag(v):
    if v in ("True", "False"):
        return v == "True"
    raise ValueError(f"not a flag: {v}")


def read_opts(opts):
    kw = {}
    head = None
    for o in opts:
        k, v = o.split("=", 1)
        if k in ("nrows", "chunksize"):
            kw[k] = int(v)
        elif k in ("convert_axes", "keep_default_dates", "precise_float", "lines"):
            kw[k] = flag(v)
        elif k == "convert_dates":
            kw[k] = flag(v) if v in ("True", "False") else v.split(",")
        elif k == "dtype":
            if v in ("True", "False"):
                kw[k] = flag(v)
            elif ":" in v:
                kw[k] = dict(p.split(":", 1) for p in v.split(","))
            else:
                kw[k] = v
        elif k == "head":
            head = int(v)
        else:
            kw[k] = v
    return kw, head


def show(obj, head):
    if isinstance(obj, pd.Series):
        print(f"series {obj.shape} {obj.dtype} name={obj.name!r}")
    else:
        print(f"shape {obj.shape}")
        for c, t in obj.dtypes.items():
            print(f"  {c!r}: {t}")
    print(f"  index: {obj.index.dtype}")
    if head is not None:
        obj = obj.head(head)
    sys.stdout.write(obj.to_csv(lineterminator="\n").replace("\r", "\\r"))


def warned(w):
    for x in w:
        msg = str(x.message).rstrip("\n")
        print(f"warn: {x.category.__name__}: {msg}")
    w.clear()


def run(job):
    w = job.split(" ")
    path = os.path.join("data", w[1])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            kw, head = read_opts(w[2:])
            if "chunksize" in kw:
                with pd.read_json(path, **kw) as reader:
                    for k, df in enumerate(reader):
                        warned(caught)
                        print(f"chunk {k}")
                        show(df, head)
                print("done")
            else:
                df = pd.read_json(path, **kw)
                warned(caught)
                show(df, head)
        except Exception as e:  # noqa: BLE001 - the job prints what pandas raised
            warned(caught)
            print(f"! {type(e).__name__}: {e}")


with open(os.path.join("data", "jobs.txt"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line:
            print(f"$ {line}")
            run(line)
