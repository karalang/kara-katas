# Cross-check: parse the same documents with Python's tomllib (3.11+),
# render them with toml_check.py's renderer, and require the same leaves;
# every BAD case must be rejected by tomllib too.
import datetime, os, sys, tempfile, tomllib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import toml_check as tc

def build(doc, v):
    if isinstance(v, dict):
        t = doc.new_table()
        for k, w in v.items():
            doc.set(t, k, build(doc, w))
        return ("table", t)
    if isinstance(v, list):
        return ("array", doc.new_array([build(doc, w) for w in v]))
    if isinstance(v, bool):
        return ("bool", v)
    if isinstance(v, int):
        return ("integer", v)
    if isinstance(v, float):
        return ("float", v)
    if isinstance(v, str):
        return ("string", v)
    if isinstance(v, datetime.datetime):
        return ("datetime" if v.tzinfo else "datetime-local", v.isoformat())
    if isinstance(v, datetime.date):
        return ("date-local", v.isoformat())
    if isinstance(v, datetime.time):
        return ("time-local", v.isoformat())
    raise TypeError(v)

ok = True
for name, text in tc.DOCS.items():
    ref = tc.Doc()
    ref.tables = []
    build(ref, tomllib.loads(text))
    mine = tc.render(tc.parse(text))
    theirs = tc.render(ref)
    if mine != theirs:
        ok = False
        print(f"MISMATCH {name}")
        for a, b in zip(mine, theirs):
            if a != b:
                print("  mine  ", a)
                print("  tomllib", b)
    else:
        print(f"ok {name}: {len(mine)} leaves")
# tomllib reads integers as Python ints of any size; TOML 1.0 requires an
# error for a value outside i64, which toml_check gives.
LENIENT = {"hex overflow"}
for label, text in tc.BAD:
    if label in LENIENT:
        continue
    try:
        tomllib.loads(text)
        ok = False
        print(f"tomllib ACCEPTED bad case: {label}")
    except tomllib.TOMLDecodeError:
        pass
print(f"ok {len(tc.BAD) - len(LENIENT)} bad cases rejected by tomllib" if ok else "FAILED")
sys.exit(0 if ok else 1)
