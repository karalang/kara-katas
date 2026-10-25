# Runs data/jobs.tsv through esprima-python 4.0.1 (the package in
# esprima/, unchanged) and prints what mini_esprima prints. Run mk.py
# first, from this directory.
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import esprima  # noqa: E402
from esprima.error_handler import Error  # noqa: E402

OPTION_NAMES = {"range": "range", "loc": "loc", "tokens": "tokens", "comment": "comment",
                "attach": "attachComment", "tolerant": "tolerant", "classProps": "classProperties"}


# ----------------------------------------------------------- JSON text
# json.dumps with separators (",", ":"), except that a compiled pattern,
# which esprima leaves in the tree and json cannot encode, is written as
# its repr.
def ser(v, out):
    if v is None:
        out.append("null")
    elif v is True:
        out.append("true")
    elif v is False:
        out.append("false")
    elif isinstance(v, (int, float, str)):
        out.append(json.dumps(v))
    elif isinstance(v, list):
        out.append("[")
        for i, x in enumerate(v):
            if i:
                out.append(",")
            ser(x, out)
        out.append("]")
    elif isinstance(v, dict):
        out.append("{")
        for i, (k, x) in enumerate(v.items()):
            if i:
                out.append(",")
            out.append(json.dumps(k))
            out.append(":")
            ser(x, out)
        out.append("}")
    elif isinstance(v, re.Pattern):
        out.append(repr(v))
    else:
        raise TypeError(type(v).__name__)


def dumps(v):
    out = []
    ser(v, out)
    return "".join(out)


def fnv(text):
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return "%08x" % h


# ------------------------------------------------------------- walking
def nodes(v):
    """Every dict with a "type", in document order."""
    if isinstance(v, dict):
        if "type" in v:
            yield v
        for x in v.values():
            yield from nodes(x)
    elif isinstance(v, list):
        for x in v:
            yield from nodes(x)


def depth(v):
    if isinstance(v, dict):
        return 1 + max([depth(x) for x in v.values()] + [0])
    if isinstance(v, list):
        return max([depth(x) for x in v] + [0])
    return 0


def counted(pairs):
    return ", ".join("%s %d" % (k, n) for k, n in pairs)


def tally(names):
    counts = {}
    for n in names:
        counts[n] = counts.get(n, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def digest(d):
    lines = []
    body = d.get("body", [])
    n = sum(1 for _ in nodes(body))
    lines.append("program: %s, %d statements, %d nodes, depth %d" % (d["sourceType"], len(body), n, depth(body)))
    text = dumps(d)
    lines.append("json: %d bytes, fnv %s" % (len(text.encode("utf-8")), fnv(text)))
    lines.append("statements: " + counted(tally(s["type"] for s in body)))
    if "comments" in d:
        lines.append("comments: %d (%s)" % (len(d["comments"]), counted(tally(c["type"] for c in d["comments"]))))
    attached = 0
    for x in nodes(body):
        for k in ("leadingComments", "trailingComments", "innerComments"):
            attached += len(x.get(k, []))
    if attached:
        lines.append("attached comments: %d" % attached)
    if "tokens" in d:
        lines.append("tokens: %d (%s)" % (len(d["tokens"]), counted(tally(t["type"] for t in d["tokens"]))))
    for e in d.get("errors", []):
        lines.append("error: " + dumps(e))
    return lines


# ------------------------------------------------------------- outline
def expr_text(e):
    if e is None:
        return ""
    t = e["type"]
    if t == "Identifier":
        return e["name"]
    if t == "Literal":
        return e["raw"]
    if t == "ThisExpression":
        return "this"
    if t == "MemberExpression":
        if e["computed"]:
            return expr_text(e["object"]) + "[" + expr_text(e["property"]) + "]"
        return expr_text(e["object"]) + "." + expr_text(e["property"])
    if t == "CallExpression":
        return expr_text(e["callee"]) + "(" + ", ".join(expr_text(a) for a in e["arguments"]) + ")"
    return "<" + t + ">"


def param_text(p):
    t = p["type"]
    if t == "Identifier":
        return p["name"]
    if t == "AssignmentPattern":
        return param_text(p["left"]) + "="
    if t == "RestElement":
        return "..." + param_text(p["argument"])
    if t == "ObjectPattern":
        return "{…}"
    if t == "ArrayPattern":
        return "[…]"
    return "<" + t + ">"


def params(f):
    return "(" + ", ".join(param_text(p) for p in f["params"]) + ")"


def key_text(key, computed):
    if computed:
        return "[" + expr_text(key) + "]"
    return expr_text(key)


FUNCS = ("FunctionExpression", "ArrowFunctionExpression")


def fn_kind(f):
    if f["type"] == "ArrowFunctionExpression":
        word = "arrow"
    else:
        word = "function*" if f["generator"] else "function"
    return ("async " if f["async"] else "") + word


def outline_entry(n):
    t = n["type"]
    if t == "FunctionDeclaration":
        name = n["id"]["name"] if "id" in n else "(anonymous)"
        return "%s %s%s" % (fn_kind(n), name, params(n))
    if t in ("ClassDeclaration", "ClassExpression"):
        s = "class " + (n["id"]["name"] if "id" in n else "(anonymous)")
        if "superClass" in n:
            s += " extends " + expr_text(n["superClass"])
        return s
    if t == "MethodDefinition":
        f = n["value"]
        prefix = "static " if n["static"] else ""
        if n["kind"] in ("get", "set"):
            prefix += n["kind"] + " "
        elif f["async"]:
            prefix += "async "
        elif f["generator"]:
            prefix += "*"
        return prefix + key_text(n["key"], n["computed"]) + params(f)
    if t == "FieldDefinition":
        return ("static " if n["static"] else "") + "field " + key_text(n["key"], n["computed"])
    if t == "VariableDeclarator" and "init" in n and n["init"]["type"] in FUNCS:
        return "%s = %s%s" % (param_text(n["id"]), fn_kind(n["init"]), params(n["init"]))
    if t == "Property" and n["value"]["type"] in FUNCS:
        f = n["value"]
        if n["kind"] in ("get", "set"):
            return n["kind"] + " " + key_text(n["key"], n["computed"]) + params(f)
        return key_text(n["key"], n["computed"]) + ": " + fn_kind(f) + params(f)
    if t == "AssignmentExpression" and n["right"]["type"] in FUNCS:
        return "%s = %s%s" % (expr_text(n["left"]), fn_kind(n["right"]), params(n["right"]))
    return None


def outline(v, level, out):
    if isinstance(v, dict):
        entry = outline_entry(v) if "type" in v else None
        inner = level
        if entry is not None:
            out.append("%sL%d %s" % ("  " * level, v["loc"]["start"]["line"], entry))
            inner = level + 1
        for x in v.values():
            outline(x, inner, out)
    elif isinstance(v, list):
        for x in v:
            outline(x, level, out)


# --------------------------------------------------------------- stats
def stats(d):
    lines = []
    all_nodes = list(nodes(d["body"]))
    lines.append("node types: " + counted(tally(n["type"] for n in all_nodes)[:12]))
    names = [n["name"] for n in all_nodes if n["type"] == "Identifier"]
    lines.append("identifiers: %d, %d distinct; top: %s" % (len(names), len(set(names)), counted(tally(names)[:8])))
    strings = [n["value"] for n in all_nodes if n["type"] == "Literal" and isinstance(n.get("value"), str)]
    lines.append("string literals: %d, %d characters" % (len(strings), sum(len(s) for s in strings)))
    nums = [n["raw"] for n in all_nodes if n["type"] == "Literal" and type(n.get("value")) in (int, float)]
    lines.append("numeric literals: %d; distinct raw: %s" % (len(nums), " ".join(sorted(set(nums)))))
    regexes = [n["regex"]["pattern"] + "/" + n["regex"]["flags"] for n in all_nodes if "regex" in n]
    lines.append("regular expressions: %d%s" % (len(regexes), "".join("\n  /" + r for r in regexes)))
    funcs = [n for n in all_nodes if n["type"] in ("FunctionDeclaration",) + FUNCS]
    longest = 0
    for f in funcs:
        longest = max(longest, f["loc"]["end"]["line"] - f["loc"]["start"]["line"] + 1)
    lines.append("functions: %d (%d arrow, %d async, %d generator); longest %d lines" % (
        len(funcs), sum(1 for f in funcs if f["type"] == "ArrowFunctionExpression"),
        sum(1 for f in funcs if f["async"]), sum(1 for f in funcs if f["generator"]), longest))
    return lines


# --------------------------------------------------------------- graph
def resolve(base, spec):
    if not spec.startswith("./") and not spec.startswith("../"):
        return None
    parts = base.split("/")[:-1]
    for p in spec.split("/"):
        if p == "..":
            parts.pop()
        elif p != ".":
            parts.append(p)
    return "/".join(parts)


def spec_text(s):
    t = s["type"]
    if t == "ImportDefaultSpecifier":
        return "default " + s["local"]["name"]
    if t == "ImportNamespaceSpecifier":
        return "* as " + s["local"]["name"]
    if s["imported"]["name"] == s["local"]["name"]:
        return s["local"]["name"]
    return s["imported"]["name"] + " as " + s["local"]["name"]


def declared_names(decl):
    if decl["type"] == "VariableDeclaration":
        return [param_text(d["id"]) for d in decl["declarations"]]
    return [decl["id"]["name"]]


def graph(paths, trees, out):
    deps = {}
    for p in paths:
        d = trees[p]
        out.append(p)
        deps[p] = []
        exports = []
        for s in d["body"]:
            if s["type"] == "ImportDeclaration":
                src = s["source"]["value"]
                specs = ", ".join(spec_text(x) for x in s["specifiers"])
                out.append("  imports %s%s" % (src, " (" + specs + ")" if specs else ""))
                target = resolve(p, src)
                if target is not None:
                    deps[p].append(target)
            elif s["type"] == "ExportNamedDeclaration":
                if "declaration" in s:
                    exports.extend(declared_names(s["declaration"]))
                for x in s["specifiers"]:
                    exports.append(x["exported"]["name"])
                if "source" in s:
                    out.append("  re-exports from " + s["source"]["value"])
            elif s["type"] == "ExportDefaultDeclaration":
                exports.append("default")
            elif s["type"] == "ExportAllDeclaration":
                out.append("  re-exports * from " + s["source"]["value"])
        out.append("  exports " + (", ".join(exports) if exports else "nothing"))
    missing = sorted(set(t for p in paths for t in deps[p] if t not in deps))
    for m in missing:
        out.append("unresolved: " + m)
    # dependencies first; ties in path order
    order = []
    left = {p: sorted(set(t for t in deps[p] if t in deps)) for p in paths}
    while left:
        ready = sorted(p for p, ds in left.items() if all(x in order for x in ds))
        if not ready:
            out.append("cycle among: " + ", ".join(sorted(left)))
            break
        order.append(ready[0])
        del left[ready[0]]
    out.append("load order: " + " -> ".join(order))


# ---------------------------------------------------------------- jobs
def options(text, path):
    kw = {}
    for name in [x for x in text.split(",") if x]:
        if name == "source":
            kw["source"] = path
        else:
            kw[OPTION_NAMES[name]] = True
    return kw


def parse(path, mode, opts):
    code = open(os.path.join("data", "src", path), encoding="utf-8", newline="").read()
    fn = esprima.parseModule if mode == "module" else esprima.parseScript
    return fn(code, options(opts, path)).toDict()


def run(job, out):
    op, path, mode, opts = job[1], job[2], job[3], job[4]
    if op == "tree":
        out.append(dumps(parse(path, mode, opts)))
    elif op == "digest":
        out.extend(digest(parse(path, mode, opts)))
    elif op == "tokens":
        code = open(os.path.join("data", "src", path), encoding="utf-8", newline="").read()
        toks = esprima.tokenize(code, options(opts, path))
        out.append(dumps(esprima.toDict(toks)))
        if hasattr(toks, "errors"):
            out.append("errors: " + dumps(toks.errors))
    elif op == "tokens-digest":
        code = open(os.path.join("data", "src", path), encoding="utf-8", newline="").read()
        toks = esprima.toDict(esprima.tokenize(code, options(opts, path)))
        text = dumps(toks)
        out.append("tokens: %d (%s)" % (len(toks), counted(tally(t["type"] for t in toks))))
        out.append("json: %d bytes, fnv %s" % (len(text.encode("utf-8")), fnv(text)))
    elif op == "outline":
        outline(parse(path, mode, "loc,classProps")["body"], 0, out)
    elif op == "stats":
        out.extend(stats(parse(path, mode, "loc,classProps")))
    elif op == "graph":
        paths = path.split("+")
        trees = {p: parse(p, "module", "classProps") for p in paths}
        graph(paths, trees, out)


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = [line.rstrip("\n").split("\t") for line in f if not line.startswith("#")]
    for job in jobs:
        print("== job %s: %s %s %s%s" % (job[0], job[1], job[2], job[3], " [" + job[4] + "]" if job[4] else ""))
        out = []
        try:
            run(job, out)
        except Error as e:
            out.append("error: " + dumps(e.toDict()))
        except Exception as e:
            out.append("crash: %s: %s" % (type(e).__name__, e))
        for line in out:
            print(line)


main()
