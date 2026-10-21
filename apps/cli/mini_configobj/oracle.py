# Runs jobs.tsv through configobj and its validate module (the copies
# in configobj/, unchanged) and prints what mini_configobj prints.
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from configobj import ConfigObj, flatten_errors, get_extra_values  # noqa: E402
from configobj.validate import Validator  # noqa: E402

configs = {}
results = {}


def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append("\n" if n == "n" else "\t" if n == "t" else n)
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def fail(e):
    return "! %s: %s" % (type(e).__name__, e)


def show_text(s):
    return s.replace("\r", "<CR>")


def walk_to(cfg, path):
    obj = cfg
    if path:
        for seg in path.split("/"):
            obj = obj[seg]
    return obj


def parent_and_key(cfg, path):
    segs = path.split("/")
    return walk_to(cfg, "/".join(segs[:-1])), segs[-1]


def rename_transform(section, key, old, new):
    val = section[key]
    newkey = key.replace(old, new)
    section.rename(key, newkey)
    if isinstance(val, (tuple, list, dict)):
        pass
    else:
        val = val.replace(old, new)
        section[newkey] = val


def int_transform(section, key):
    section[key] = int(section[key])


def run(op, args):
    if op == "load":
        name, path, opts = args[0], args[1], json.loads(args[2])
        if "configspec" in opts:
            opts["configspec"] = "data/" + opts["configspec"]
        try:
            configs[name] = ConfigObj("data/" + path, **opts)
            print("ok")
        except Exception as e:  # noqa: BLE001
            print(fail(e))
            errs = getattr(e, "errors", None)
            if errs and len(errs) > 1:
                for x in errs:
                    print("  %s at %d: %s %r" % (type(x).__name__, x.line_number, x, x.line))
            if getattr(e, "config", None) is not None:
                configs[name] = e.config
        return
    cfg = configs.get(args[0]) if op not in ("check", "default") else None
    if op == "repr":
        print(repr(walk_to(cfg, args[1] if len(args) > 1 else "")))
    elif op == "get":
        print(repr(walk_to(cfg, args[1])))
    elif op == "keys":
        print(repr(walk_to(cfg, args[1] if len(args) > 1 else "").keys()))
    elif op == "items":
        print(repr(walk_to(cfg, args[1]).items()))
    elif op == "dict":
        print(repr(walk_to(cfg, args[1]).dict()))
    elif op == "comments":
        sec = walk_to(cfg, args[1] if len(args) > 1 else "")
        if sec is cfg:
            print("initial %r" % (cfg.initial_comment,))
        for k in sec.scalars + sec.sections:
            print("%s %r %r" % (k, sec.comments[k], sec.inline_comments[k]))
        if sec is cfg:
            print("final %r" % (cfg.final_comment,))
    elif op == "write":
        if len(args) > 1:
            for line in cfg.write(section=walk_to(cfg, args[1])):
                print(show_text(line))
        else:
            buf = io.BytesIO()
            cfg.write(outfile=buf)
            print(show_text(buf.getvalue().decode("utf-8")), end="")
            print("<EOF>")
    elif op == "set":
        sec, key = parent_and_key(cfg, args[1])
        sec[key] = json.loads(args[2])
        print("ok")
    elif op == "rename":
        walk_to(cfg, args[1]).rename(args[2], args[3])
        print("ok")
    elif op == "del":
        sec, key = parent_and_key(cfg, args[1])
        del sec[key]
        print("ok")
    elif op == "pop":
        sec, key = parent_and_key(cfg, args[1])
        print(repr(sec.pop(key)))
    elif op == "setdefault":
        sec, key = parent_and_key(cfg, args[1])
        print(repr(sec.setdefault(key, args[2])))
    elif op == "popitem":
        print(repr(walk_to(cfg, args[1]).popitem()))
    elif op == "merge":
        cfg.merge(configs[args[1]])
        print("ok")
    elif op == "walk_rename":
        print(repr(cfg.walk(rename_transform, call_on_sections=True, old=args[1], new=args[2])))
    elif op == "walk_int":
        print(repr(cfg.walk(int_transform, raise_errors=args[1] == "strict")))
    elif op == "validate":
        r = cfg.validate(Validator(), **json.loads(args[1]))
        results[args[0]] = r
        print(repr(r))
    elif op == "flatten":
        for t in flatten_errors(cfg, results[args[0]]):
            print(repr(t))
    elif op == "extra":
        print(repr(get_extra_values(cfg)))
    elif op == "restore_defaults":
        cfg.restore_defaults()
        print("ok")
    elif op == "check":
        value = json.loads(args[1])
        print(repr(Validator().check(args[0], value, missing=value is None)))
    elif op == "default":
        print(repr(Validator().get_default_value(args[0])))
    elif op.startswith("as_"):
        sec, key = parent_and_key(cfg, args[1])
        print(repr(getattr(sec, op)(key)))


with open("data/jobs.tsv", encoding="utf-8") as f:
    lines = f.read().split("\n")
for line in lines:
    if not line:
        continue
    if line.startswith("== "):
        print(line)
        continue
    raw = line.split("\t")
    parts = [unesc(x) for x in raw]
    print("-- " + " ".join(raw))
    try:
        run(parts[0], parts[1:])
    except Exception as e:  # noqa: BLE001
        print(fail(e))
