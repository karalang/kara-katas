# Runs data/jobs.tsv through Apache Avro 1.12.0 (the avro/ package next to
# this file, unchanged) and prints what it did. mini_avro.kara must print
# the same bytes.
#
# Avro's messages are printed as Avro builds them, with two changes:
#  - a message that names a Python object prints "<avro.schema.X object>"
#    where Python prints the object's address, which changes every run;
#  - "\r" prints as the two characters \r (CSV rows end in \r\n).
#
# Values read back are printed by show(): Python's repr, except that a
# date, time or datetime prints as date(...), time(...) or datetime(...)
# around its isoformat(), since a datetime's repr names its tzinfo object.
import csv
import datetime
import decimal
import hashlib
import io
import json
import os
import re
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import avro.__main__  # noqa: E402
import avro.datafile  # noqa: E402
import avro.io  # noqa: E402
import avro.schema  # noqa: E402

SYNC = bytes.fromhex("8e3a5f9c01d24b67a9f0c3e15d7b2846")
avro.datafile.randbytes = lambda n: SYNC[:n]

OUT = []


def emit(s):
    OUT.append(s)


def clean(msg):
    msg = re.sub(r" object at 0x[0-9a-fA-F]+>", " object>", msg)
    return msg.replace("\r", "\\r")


def err(e):
    return "error: %s: %s" % (type(e).__name__, clean(str(e)))


def warns(ws, indent=""):
    for w in ws:
        emit("%swarning: %s: %s" % (indent, type(w.message).__name__, clean(str(w.message))))


def to_py(j):
    if isinstance(j, dict):
        if len(j) == 1:
            (k, v), = j.items()
            if k == "$bytes":
                return bytes.fromhex(v)
            if k == "$decimal":
                return decimal.Decimal(v)
            if k == "$date":
                return datetime.date.fromisoformat(v)
            if k == "$time":
                return datetime.time.fromisoformat(v)
            if k in ("$datetime", "$naive"):
                return datetime.datetime.fromisoformat(v)
        return {k: to_py(v) for k, v in j.items()}
    if isinstance(j, list):
        return [to_py(v) for v in j]
    return j


def show(v):
    if isinstance(v, datetime.datetime):
        return "datetime(%s)" % v.isoformat()
    if isinstance(v, datetime.date):
        return "date(%s)" % v.isoformat()
    if isinstance(v, datetime.time):
        return "time(%s)" % v.isoformat()
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join("%r: %s" % (k, show(x)) for k, x in v.items()) + "}"
    return repr(v)


def read_text(rel):
    with open(os.path.join(HERE, "data", rel), encoding="utf-8") as f:
        return f.read()


def load_schema(rel, label):
    s, e, ws = capture(lambda: avro.schema.parse(read_text(rel)))
    warns(ws)
    if e is not None:
        emit((label + " " if label else "") + err(e))
    return s


def datums(rel):
    return [to_py(json.loads(line)) for line in read_text(rel).splitlines() if line]


def encode(s, d):
    buf = io.BytesIO()
    avro.io.DatumWriter(s).write(d, avro.io.BinaryEncoder(buf))
    return buf.getvalue()


def decode(w, r, data):
    buf = io.BytesIO(data)
    v = avro.io.DatumReader(w, r).read(avro.io.BinaryDecoder(buf))
    return v, len(data) - buf.tell()


def capture(fn):
    # Runs fn, returning (result, exception, warnings raised).
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        warnings.simplefilter("ignore", ResourceWarning)
        try:
            r = fn()
        except Exception as e:
            return None, e, ws
    return r, None, ws


def schema_job(rel):
    s = load_schema(rel, "")
    if s is None:
        return
    emit("json: " + str(s))
    emit("canonical: " + s.canonical_form)
    emit("crc64: " + s.fingerprint().hex())
    emit("md5: " + s.fingerprint("md5").hex())
    emit("sha256: " + s.fingerprint("sha256").hex())


def vectors_job():
    for i, line in enumerate(read_text("vectors.txt").splitlines()):
        s, e, ws = capture(lambda: avro.schema.parse(line))
        if e is not None:
            emit("[%d] %s" % (i, err(e)))
            warns(ws, "  ")
            continue
        emit("[%d] %s" % (i, s.fingerprint().hex()))
        warns(ws, "  ")
        emit("  json: " + str(s))
        emit("  canonical: " + s.canonical_form)


def encode_job(srel, drel):
    s = load_schema(srel, "schema")
    if s is None:
        return
    for i, d in enumerate(datums(drel)):
        data, e, ws = capture(lambda: encode(s, d))
        emit("[%d] %s" % (i, data.hex() if e is None else err(e)))
        warns(ws, "  ")
        if e is not None:
            continue
        r, e, ws = capture(lambda: decode(s, s, data))
        emit("  -> " + (show(r[0]) if e is None else err(e)))
        warns(ws, "  ")


def resolve_job(wrel, rrel, drel):
    w = load_schema(wrel, "writer")
    r = load_schema(rrel, "reader")
    if w is None or r is None:
        return
    for i, d in enumerate(datums(drel)):
        data, e, ws = capture(lambda: encode(w, d))
        if e is not None:
            emit("[%d] write %s" % (i, err(e)))
            warns(ws, "  ")
            continue
        warns(ws, "  ")
        v, e, ws = capture(lambda: decode(w, r, data))
        emit("[%d] -> %s" % (i, show(v[0]) if e is None else err(e)))
        warns(ws, "  ")


def decode_job(srel, brel):
    s = load_schema(srel, "schema")
    if s is None:
        return
    with open(os.path.join(HERE, "data", brel), "rb") as f:
        data = f.read()
    v, e, ws = capture(lambda: decode(s, s, data))
    warns(ws)
    if e is not None:
        emit(err(e))
        return
    emit("-> " + show(v[0]))
    emit("rest: %d bytes" % v[1])


def read_file(f, reader_schema, indent=""):
    def opened():
        return avro.datafile.DataFileReader(f, avro.io.DatumReader(readers_schema=reader_schema))
    dfr, e, ws = capture(opened)
    warns(ws, indent)
    if e is not None:
        emit(indent + err(e))
        return
    emit(indent + "codec: " + dfr.codec)
    emit(indent + "meta: " + ", ".join(dfr.meta.keys()))
    emit(indent + "schema: " + str(dfr.datum_reader.writers_schema))
    n = 0
    it = iter(dfr)
    while True:
        v, e, ws = capture(lambda: next(it))
        warns(ws, indent + "  ")
        if isinstance(e, StopIteration):
            break
        if e is not None:
            emit(indent + err(e))
            break
        emit(indent + "  " + show(v))
        n += 1
    emit(indent + "records: %d" % n)


def read_job(frel, srel=None):
    r = None
    if srel is not None:
        r = load_schema(srel, "reader")
        if r is None:
            return
    with open(os.path.join(HERE, "data", frel), "rb") as f:
        read_file(f, r)


def write_job(srel, drel):
    s = load_schema(srel, "schema")
    if s is None:
        return
    buf = io.BytesIO()
    w = avro.datafile.DataFileWriter(buf, avro.io.DatumWriter(), s)
    for i, d in enumerate(datums(drel)):
        _, e, ws = capture(lambda: w.append(d))
        if e is not None:
            emit("[%d] %s" % (i, err(e)))
        warns(ws, "  ")
    w.flush()
    data = buf.getvalue()
    emit("bytes: %d sha256: %s" % (len(data), hashlib.sha256(data).hexdigest()))
    read_file(io.BytesIO(data), None)


def cli(args, out_path=None):
    stdout = io.StringIO()
    saved = sys.stdout, avro.__main__._write_row
    sys.stdout = stdout
    avro.__main__._write_row = csv.writer(stdout).writerow
    sys.argv = ["avro"] + args
    try:
        try:
            code = avro.__main__.main()
            result = "exit: %d" % code
        except Exception as e:
            result = err(e)
    finally:
        sys.stdout, avro.__main__._write_row = saved
    for line in stdout.getvalue().split("\n")[:-1] if stdout.getvalue() else []:
        emit("| " + clean(line))
    if stdout.getvalue() and not stdout.getvalue().endswith("\n"):
        emit("| " + clean(stdout.getvalue().split("\n")[-1]) + " (no newline)")
    emit(result)


def tool_write_job(args):
    out_path = os.path.join(HERE, "data", "out.avro")
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        warnings.simplefilter("ignore", ResourceWarning)
        cli(["write"] + args + ["-o", out_path])
    warns(ws)
    with open(out_path, "rb") as f:
        data = f.read()
    os.remove(out_path)
    emit("bytes: %d sha256: %s" % (len(data), hashlib.sha256(data).hexdigest()))
    if data:
        read_file(io.BytesIO(data), None)


def main():
    os.chdir(HERE)
    for line in read_text("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        kind, rest = job[0], job[1:]
        if kind == "schema":
            schema_job(*rest)
        elif kind == "vectors":
            vectors_job()
        elif kind == "encode":
            encode_job(*rest)
        elif kind == "resolve":
            resolve_job(*rest)
        elif kind == "decode":
            decode_job(*rest)
        elif kind == "read":
            read_job(*rest)
        elif kind == "write":
            write_job(*rest)
        elif kind == "cat":
            with warnings.catch_warnings(record=True) as ws:
                warnings.simplefilter("always")
                warnings.simplefilter("ignore", ResourceWarning)
                cli(job)
            warns(ws)
        elif kind == "tool-write":
            tool_write_job(rest)
    sys.stdout.write("".join(s + "\n" for s in OUT))


if __name__ == "__main__":
    main()
