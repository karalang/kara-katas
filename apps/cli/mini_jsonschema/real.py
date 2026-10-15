# Runs data/jobs.txt with the real Python jsonschema 4.26 library (Draft
# 2020-12) and Python's json module: the same `validate` tool, written on them.
import json, os, sys
import jsonschema
from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

base = os.path.abspath("data")
out = []

def show(e, indent):
    path = "/".join(str(p) for p in e.relative_schema_path)
    out.append(f"{' ' * indent}{'- ' if indent > 2 else ''}{e.json_path}: {e.message} ({path})\n")
    for c in sorted(e.context, key=lambda c: (c.json_path, "/".join(str(p) for p in c.relative_schema_path), c.message)):
        show(c, indent + 2)

def load(rel):
    p = os.path.join(base, rel)
    if not os.path.isfile(p):
        return None, f"{rel}: No such file or directory"
    try:
        return json.loads(open(p, encoding="utf-8").read()), None
    except json.JSONDecodeError as e:
        return None, f"{rel}: {e}"

def validate(args):
    best = False
    if args and args[0] == "--best":
        best = True
        args = args[1:]
    if len(args) < 2:
        out.append("usage: validate [--best] SCHEMA DOC...\n")
        return 2
    schema, err = load(args[0])
    if err:
        out.append(err + "\n")
        return 2
    v = Draft202012Validator(schema)
    rc = 0
    for rel in args[1:]:
        inst, err = load(rel)
        if err:
            out.append(err + "\n")
            rc = 2
            continue
        errors = list(v.iter_errors(inst))
        if not errors:
            out.append(f"{rel}: valid\n")
            continue
        rc = max(rc, 1)
        if best:
            e = best_match(errors)
            out.append(f"{rel}: {e.json_path}: {e.message}\n")
            continue
        n = len(errors)
        out.append(f"{rel}: {n} error{'s' if n != 1 else ''}\n")
        for e in sorted(errors, key=lambda e: (e.json_path, "/".join(str(p) for p in e.relative_schema_path), e.message)):
            show(e, 2)
    return rc

for line in open("data/jobs.txt").read().splitlines():
    if not line or line.startswith("#"):
        continue
    out.append(f"$ {line}\n")
    parts = line.split(" ")
    rc = validate(parts[1:])
    if rc:
        out.append(f"[exit status {rc}]\n")
    out.append("\n")
sys.stdout.write("".join(out))
