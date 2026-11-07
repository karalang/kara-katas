"""Reference for mini_alembic. Reads data/ (as mk.py writes it), writes
data/out/, and prints the report the Kāra program must print.

Run from this directory: python3 -I -B oracle.py"""
import os
import shutil

TYPES = ["int", "text", "real", "bool", "date"]
SQL_TYPES = {"int": "INTEGER", "text": "TEXT", "real": "REAL", "bool": "BOOLEAN", "date": "DATE"}
USAGE = {
    "create_table": "create_table <table> <column>...",
    "drop_table": "drop_table <table>",
    "add_column": "add_column <table> <column>",
    "drop_column": "drop_column <table> <column>",
    "rename_table": "rename_table <old> <new>",
    "rename_column": "rename_column <table> <old> <new>",
    "alter_column": "alter_column <table> <column> <change>...",
    "create_index": "create_index <index> <table> <columns> [unique]",
    "drop_index": "drop_index <index>",
    "execute": "execute <sql>",
}
OUT = []


def say(s):
    OUT.append(s)


class Bad(Exception):
    pass


# ------------------------------------------------------------ parsing


def is_name(s):
    return (0 < len(s) <= 30 and (s[0].isascii() and (s[0].islower() or s[0] == "_"))
            and all(c == "_" or (c.isascii() and (c.islower() or c.isdigit())) for c in s))


def need_name(s):
    if not is_name(s):
        raise Bad(f"bad name '{s}'")
    return s


def is_rev(s):
    return 6 <= len(s) <= 12 and all(c in "0123456789abcdef" for c in s)


def is_label(s):
    return (0 < len(s) <= 24 and s[0].isascii() and s[0].islower()
            and all(c == "_" or (c.isascii() and (c.islower() or c.isdigit())) for c in s)
            and s not in ("head", "heads", "base"))


def parse_column(spec, allow_pk=True):
    parts = spec.split(":")
    if len(parts) < 2:
        raise Bad(f"bad column '{spec}'")
    name = need_name(parts[0])
    if parts[1] not in TYPES:
        raise Bad(f"unknown type '{parts[1]}'")
    col = {"name": name, "type": parts[1], "pk": False, "notnull": False, "default": None}
    seen = []
    for f in parts[2:]:
        key = "default" if f.startswith("default=") else f
        if key in seen:
            raise Bad(f"duplicate flag '{key}'")
        seen.append(key)
        if f == "pk":
            if not allow_pk:
                raise Bad("add_column cannot add a primary key")
            col["pk"] = True
        elif f == "notnull":
            col["notnull"] = True
        elif key == "default":
            v = f[len("default="):]
            if v == "":
                raise Bad(f"bad default in '{spec}'")
            col["default"] = v
        else:
            raise Bad(f"unknown flag '{f}'")
    return col


def parse_op(text):
    w = text.split()
    op = w[0]
    if op not in USAGE:
        raise Bad(f"unknown operation '{op}'")
    n = len(w) - 1
    ok = {"create_table": n >= 2, "drop_table": n == 1, "add_column": n == 2,
          "drop_column": n == 2, "rename_table": n == 2, "rename_column": n == 3,
          "alter_column": n >= 3, "create_index": n in (3, 4), "drop_index": n == 1,
          "execute": n >= 1}[op]
    if not ok:
        raise Bad(f"usage: {USAGE[op]}")
    o = {"op": op, "text": text}
    if op == "create_table":
        o["table"] = need_name(w[1])
        cols = []
        for spec in w[2:]:
            c = parse_column(spec)
            if any(x["name"] == c["name"] for x in cols):
                raise Bad(f"duplicate column '{c['name']}'")
            cols.append(c)
        o["cols"] = cols
    elif op == "drop_table":
        o["table"] = need_name(w[1])
    elif op == "add_column":
        o["table"] = need_name(w[1])
        o["col"] = parse_column(w[2], allow_pk=False)
    elif op == "drop_column":
        o["table"] = need_name(w[1])
        o["column"] = need_name(w[2])
    elif op == "rename_table":
        o["table"] = need_name(w[1])
        o["new"] = need_name(w[2])
    elif op == "rename_column":
        o["table"] = need_name(w[1])
        o["column"] = need_name(w[2])
        o["new"] = need_name(w[3])
    elif op == "alter_column":
        o["table"] = need_name(w[1])
        o["column"] = need_name(w[2])
        ch = []
        for c in w[3:]:
            if c.startswith("type="):
                t = c[len("type="):]
                if t not in TYPES:
                    raise Bad(f"unknown type '{t}'")
                ch.append(("type", t))
            elif c in ("notnull", "null"):
                ch.append((c, ""))
            else:
                raise Bad(f"unknown change '{c}'")
        o["changes"] = ch
    elif op == "create_index":
        o["index"] = need_name(w[1])
        o["table"] = need_name(w[2])
        cols = []
        for c in w[3].split(","):
            need_name(c)
            if c in cols:
                raise Bad(f"column '{c}' listed twice")
            cols.append(c)
        o["cols"] = cols
        if n == 4 and w[4] != "unique":
            raise Bad(f"expected 'unique', found '{w[4]}'")
        o["unique"] = n == 4
    elif op == "drop_index":
        o["index"] = need_name(w[1])
    else:
        o["sql"] = text[len("execute"):].strip()
    return o


def parse_mig(path, text):
    """A revision, or an error line."""
    name = os.path.basename(path)
    keys = {}
    section = None
    seen_sections = []
    ops = {"upgrade": [], "downgrade": []}
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip()
        s = line.strip()
        if s == "" or s.startswith("#"):
            continue
        try:
            if line[0] in " \t":
                if section is None:
                    raise Bad("operation outside upgrade/downgrade")
                ops[section].append(parse_op(s))
                continue
            if s in ("upgrade:", "downgrade:"):
                sec = s[:-1]
                if sec in seen_sections:
                    raise Bad(f"duplicate section '{sec}'")
                seen_sections.append(sec)
                section = sec
                continue
            first = s.split()[0]
            if first in USAGE:
                raise Bad("operation outside upgrade/downgrade" if section is None
                          else "operation must be indented")
            if section is not None:
                raise Bad("key after the upgrade/downgrade sections")
            at = s.find(":")
            key = s[:at] if at > 0 else ""
            if (at <= 0 or not all(c == "_" or ("a" <= c <= "z") for c in key)
                    or not (at + 1 == len(s) or s[at + 1] == " ")):
                raise Bad("expected key: value")
            value = s[at + 1:].strip()
            if key not in ("revision", "down", "label", "message"):
                raise Bad(f"unknown key '{key}'")
            if key in keys:
                raise Bad(f"duplicate key '{key}'")
            if key == "revision" and not is_rev(value):
                raise Bad(f"bad revision id '{value}'")
            if key == "down":
                if value == "none":
                    value = []
                else:
                    ds = [d.strip() for d in value.split(",")]
                    out = []
                    for d in ds:
                        if not is_rev(d):
                            raise Bad(f"bad revision id '{d}'")
                        if d in out:
                            raise Bad(f"down lists {d} twice")
                        out.append(d)
                    value = out
            if key == "label" and not is_label(value):
                raise Bad(f"bad label '{value}'")
            if key == "message" and value == "":
                raise Bad("empty message")
            keys[key] = value
        except Bad as e:
            return f"{path}:{i}: {e}"
    for k in ("revision", "down", "message"):
        if k not in keys:
            return f"{path}: missing {k}"
    for sec in ("upgrade", "downgrade"):
        if sec not in seen_sections:
            return f"{path}: missing {sec}"
    if not name.startswith(keys["revision"] + "_"):
        return f"{path}: file name does not start with revision {keys['revision']}"
    return {"rev": keys["revision"], "down": keys["down"], "label": keys.get("label"),
            "message": keys["message"], "path": path, "up": ops["upgrade"],
            "dn": ops["downgrade"]}


# ------------------------------------------------------------ the graph


class Graph:
    def __init__(self, revs):
        self.revs = {r["rev"]: r for r in revs}
        self.children = {r: [] for r in self.revs}
        for r in self.revs.values():
            for d in r["down"]:
                self.children[d].append(r["rev"])
        for c in self.children.values():
            c.sort()
        placed = set()
        order = []
        ready = sorted(r for r, x in self.revs.items() if not x["down"])
        while ready:
            ready.sort()
            r = ready.pop(0)
            placed.add(r)
            order.append(r)
            for c in self.children[r]:
                if all(d in placed for d in self.revs[c]["down"]):
                    ready.append(c)
        self.order = order
        self.pos = {r: i for i, r in enumerate(order)}
        self.heads = [r for r in order if not self.children[r]]
        self.labels = {x["label"]: r for r, x in self.revs.items() if x["label"]}

    def ancestors(self, targets):
        out = set()
        stack = list(targets)
        while stack:
            r = stack.pop()
            if r not in out:
                out.add(r)
                stack.extend(self.revs[r]["down"])
        return out

    def descendants(self, r):
        out = set()
        stack = list(self.children[r])
        while stack:
            x = stack.pop()
            if x not in out:
                out.add(x)
                stack.extend(self.children[x])
        return out

    def by_pos(self, s, rev=False):
        return sorted(s, key=lambda r: self.pos[r], reverse=rev)

    def current(self, applied):
        return [r for r in self.order
                if r in applied and not any(c in applied for c in self.children[r])]

    def resolve(self, spec):
        """A revision id, None for base, or Bad."""
        if spec == "base":
            return None
        if spec == "head":
            if len(self.heads) != 1:
                raise Bad(f"multiple heads ({', '.join(self.heads)}); name one or use heads")
            return self.heads[0]
        if "@" in spec:
            label, rest = spec.split("@", 1)
            if rest != "head":
                raise Bad(f"bad revision '{spec}'")
            if label not in self.labels:
                raise Bad(f"no label '{label}'")
            r = self.labels[label]
            hs = [h for h in self.heads if h == r or h in self.descendants(r)]
            if len(hs) != 1:
                raise Bad(f"label {label} has {len(hs)} heads ({', '.join(hs)})")
            return hs[0]
        if spec in self.labels:
            return self.labels[spec]
        if spec == "" or not all(c in "0123456789abcdef" for c in spec):
            raise Bad(f"no revision '{spec}'")
        if spec in self.revs:
            return spec
        if len(spec) < 3:
            raise Bad(f"revision prefix '{spec}' is too short")
        m = sorted(r for r in self.revs if r.startswith(spec))
        if not m:
            raise Bad(f"no revision '{spec}'")
        if len(m) > 1:
            raise Bad(f"ambiguous revision '{spec}' ({', '.join(m)})")
        return m[0]


def load_revisions(verbose):
    files = []
    for d, shown in (("data/out/versions", "out/versions"), ("data/versions", "versions")):
        if os.path.isdir(d):
            for n in os.listdir(d):
                if n.endswith(".mig"):
                    files.append((f"{shown}/{n}", f"{d}/{n}"))
    files.sort()
    errors = []
    parsed = []
    for shown, real in files:
        with open(real, encoding="utf-8", newline="") as fh:
            r = parse_mig(shown, fh.read())
        if isinstance(r, str):
            errors.append((shown, r))
        else:
            parsed.append(r)
    keep = []
    first = {}
    for r in parsed:
        if r["rev"] in first:
            errors.append((r["path"], f"{r['path']}: revision {r['rev']} already defined in {first[r['rev']]}"))
        else:
            first[r["rev"]] = r["path"]
            keep.append(r)
    labels = {}
    k2 = []
    for r in keep:
        if r["label"] and r["label"] in labels:
            errors.append((r["path"], f"{r['path']}: label {r['label']} already used by {labels[r['label']]}"))
        else:
            if r["label"]:
                labels[r["label"]] = r["rev"]
            k2.append(r)
    keep = k2
    while True:
        have = {r["rev"] for r in keep}
        nxt = []
        for r in keep:
            miss = [d for d in r["down"] if d not in have]
            if miss:
                errors.append((r["path"], f"{r['path']}: down revision {miss[0]} not found"))
            else:
                nxt.append(r)
        if len(nxt) == len(keep):
            break
        keep = nxt
    grounded = set()
    changed = True
    while changed:
        changed = False
        for r in keep:
            if r["rev"] not in grounded and all(d in grounded for d in r["down"]):
                grounded.add(r["rev"])
                changed = True
    k3 = []
    for r in keep:
        if r["rev"] in grounded:
            k3.append(r)
        else:
            errors.append((r["path"], f"{r['path']}: revision {r['rev']} does not lead back to a base"))
    errors.sort(key=lambda e: e[0])
    if verbose:
        for _, e in errors:
            say(e)
    say(("" if verbose else "  ") + f"loaded {len(k3)} revisions from {len(files)} files, {len(errors)} skipped")
    return Graph(k3)


# ------------------------------------------------------------ the schema


def col_text(c):
    s = f"{c['name']} {c['type']}"
    if c["pk"]:
        s += " pk"
    if c["notnull"]:
        s += " notnull"
    if c["default"] is not None:
        s += f" default={c['default']}"
    return s


def schema_lines(sc):
    out = []
    for t in sorted(sc["tables"]):
        out.append(f"table {t} ({', '.join(col_text(c) for c in sc['tables'][t])})")
    for ix in sorted(sc["indexes"]):
        t, cols, u = sc["indexes"][ix]
        out.append(f"index {ix} on {t} ({', '.join(cols)})" + (" unique" if u else ""))
    return out


def copy_schema(sc):
    return {"tables": {t: [dict(c) for c in cs] for t, cs in sc["tables"].items()},
            "indexes": {i: (t, list(c), u) for i, (t, c, u) in sc["indexes"].items()}}


def find_col(sc, t, c):
    if t not in sc["tables"]:
        raise Bad(f"no table {t}")
    for x in sc["tables"][t]:
        if x["name"] == c:
            return x
    raise Bad(f"no column {t}.{c}")


def apply_op(sc, o):
    op = o["op"]
    T = sc["tables"]
    I = sc["indexes"]
    if op == "create_table":
        if o["table"] in T:
            raise Bad(f"table {o['table']} already exists")
        T[o["table"]] = [dict(c) for c in o["cols"]]
    elif op == "drop_table":
        t = o["table"]
        if t not in T:
            raise Bad(f"no table {t}")
        for ix in sorted(I):
            if I[ix][0] == t:
                raise Bad(f"table {t} still has index {ix}")
        del T[t]
    elif op == "add_column":
        t = o["table"]
        c = o["col"]
        if t not in T:
            raise Bad(f"no table {t}")
        if any(x["name"] == c["name"] for x in T[t]):
            raise Bad(f"column {t}.{c['name']} already exists")
        if c["notnull"] and c["default"] is None:
            raise Bad(f"column {t}.{c['name']} is not null and has no default")
        T[t].append(dict(c))
    elif op == "drop_column":
        t, c = o["table"], o["column"]
        x = find_col(sc, t, c)
        if x["pk"]:
            raise Bad(f"cannot drop primary key column {t}.{c}")
        for ix in sorted(I):
            if I[ix][0] == t and c in I[ix][1]:
                raise Bad(f"column {t}.{c} is used by index {ix}")
        if len(T[t]) == 1:
            raise Bad(f"cannot drop the last column of {t}")
        T[t] = [y for y in T[t] if y["name"] != c]
    elif op == "rename_table":
        t, n = o["table"], o["new"]
        if t not in T:
            raise Bad(f"no table {t}")
        if n in T:
            raise Bad(f"table {n} already exists")
        T[n] = T.pop(t)
        for ix in list(I):
            if I[ix][0] == t:
                I[ix] = (n, I[ix][1], I[ix][2])
    elif op == "rename_column":
        t, c, n = o["table"], o["column"], o["new"]
        x = find_col(sc, t, c)
        if any(y["name"] == n for y in T[t]):
            raise Bad(f"column {t}.{n} already exists")
        x["name"] = n
        for ix in list(I):
            if I[ix][0] == t:
                I[ix] = (t, [n if y == c else y for y in I[ix][1]], I[ix][2])
    elif op == "alter_column":
        t, c = o["table"], o["column"]
        x = find_col(sc, t, c)
        for k, v in o["changes"]:
            if k == "type":
                x["type"] = v
            elif k == "notnull":
                x["notnull"] = True
            else:
                if x["pk"]:
                    raise Bad("a primary key column cannot be null")
                x["notnull"] = False
    elif op == "create_index":
        ix, t = o["index"], o["table"]
        if ix in I:
            raise Bad(f"index {ix} already exists")
        if t not in T:
            raise Bad(f"no table {t}")
        for c in o["cols"]:
            find_col(sc, t, c)
        I[ix] = (t, list(o["cols"]), o["unique"])
    elif op == "drop_index":
        if o["index"] not in I:
            raise Bad(f"no index {o['index']}")
        del I[o["index"]]


def sql_value(v):
    if v in ("true", "false") or all(c.isdigit() or c == "." for c in v) and any(c.isdigit() for c in v):
        return v
    return "'" + v + "'"


def col_sql(c):
    s = f"{c['name']} {SQL_TYPES[c['type']]}"
    if c["notnull"] or c["pk"]:
        s += " NOT NULL"
    if c["default"] is not None:
        s += f" DEFAULT {sql_value(c['default'])}"
    return s


def op_sql(o):
    op = o["op"]
    if op == "create_table":
        parts = [col_sql(c) for c in o["cols"]]
        pk = [c["name"] for c in o["cols"] if c["pk"]]
        if pk:
            parts.append(f"PRIMARY KEY ({', '.join(pk)})")
        return [f"CREATE TABLE {o['table']} ({', '.join(parts)});"]
    if op == "drop_table":
        return [f"DROP TABLE {o['table']};"]
    if op == "add_column":
        return [f"ALTER TABLE {o['table']} ADD COLUMN {col_sql(o['col'])};"]
    if op == "drop_column":
        return [f"ALTER TABLE {o['table']} DROP COLUMN {o['column']};"]
    if op == "rename_table":
        return [f"ALTER TABLE {o['table']} RENAME TO {o['new']};"]
    if op == "rename_column":
        return [f"ALTER TABLE {o['table']} RENAME COLUMN {o['column']} TO {o['new']};"]
    if op == "alter_column":
        out = []
        for k, v in o["changes"]:
            head = f"ALTER TABLE {o['table']} ALTER COLUMN {o['column']}"
            if k == "type":
                out.append(f"{head} TYPE {SQL_TYPES[v]};")
            elif k == "notnull":
                out.append(f"{head} SET NOT NULL;")
            else:
                out.append(f"{head} DROP NOT NULL;")
        return out
    if op == "create_index":
        u = "UNIQUE " if o["unique"] else ""
        return [f"CREATE {u}INDEX {o['index']} ON {o['table']} ({', '.join(o['cols'])});"]
    if op == "drop_index":
        return [f"DROP INDEX {o['index']};"]
    s = o["sql"]
    return [s if s.endswith(";") else s + ";"]


def run_steps(sc, ops):
    """None, or (step, op, message). Leaves sc changed only on success."""
    work = copy_schema(sc)
    for k, o in enumerate(ops, 1):
        try:
            apply_op(work, o)
        except Bad as e:
            return (k, o["op"], str(e))
    sc["tables"] = work["tables"]
    sc["indexes"] = work["indexes"]
    return None


# ------------------------------------------------------------ the broker of versions


STATE = "data/out/state.txt"


class Env:
    def __init__(self, g):
        self.g = g
        self.applied = set()
        self.schema = {"tables": {}, "indexes": {}}

    def cur_text(self):
        cur = self.g.current(self.applied)
        if not cur:
            return "base"
        return ", ".join(r + (" (head)" if r in self.g.heads else "") for r in cur)

    def from_text(self, r):
        d = self.g.revs[r]["down"]
        return ", ".join(d) if d else "base"

    def save(self):
        lines = [f"version {r}" for r in self.g.current(self.applied)]
        for t in sorted(self.schema["tables"]):
            lines.append(f"table {t}")
            for c in self.schema["tables"][t]:
                lines.append(f"column {col_text(c)}")
        for ix in sorted(self.schema["indexes"]):
            t, cols, u = self.schema["indexes"][ix]
            lines.append(f"index {ix} {t} {','.join(cols)}" + (" unique" if u else ""))
        with open(STATE, "w", encoding="utf-8", newline="") as fh:
            fh.write("".join(l + "\n" for l in lines))

    def restore(self):
        with open(STATE, encoding="utf-8", newline="") as fh:
            text = fh.read()
        heads = []
        sc = {"tables": {}, "indexes": {}}
        table = None
        for line in text.split("\n"):
            if line == "":
                continue
            w = line.split()
            if w[0] == "version":
                if w[1] not in self.g.revs:
                    raise Bad(f"state: version {w[1]} not found")
                heads.append(w[1])
            elif w[0] == "table":
                table = w[1]
                sc["tables"][table] = []
            elif w[0] == "column":
                c = {"name": w[1], "type": w[2], "pk": False, "notnull": False, "default": None}
                for f in w[3:]:
                    if f == "pk":
                        c["pk"] = True
                    elif f == "notnull":
                        c["notnull"] = True
                    else:
                        c["default"] = f[len("default="):]
                sc["tables"][table].append(c)
            else:
                sc["indexes"][w[1]] = (w[2], w[3].split(","), len(w) == 5)
        self.applied = self.g.ancestors(heads)
        self.schema = sc

    def targets(self, spec, what):
        """The revisions an upgrade-like command aims at."""
        if spec == "heads":
            return list(self.g.heads)
        if spec.startswith("+") and spec[1:].isdigit() and int(spec[1:]) > 0:
            n = int(spec[1:])
            cur = self.g.current(self.applied)
            if len(cur) > 1:
                raise Bad("multiple current heads; name a target")
            at = cur[0] if cur else None
            for _ in range(n):
                cand = self.g.children[at] if at else [r for r in self.g.order if not self.g.revs[r]["down"]]
                if not cand:
                    raise Bad(f"relative revision {spec} goes past the head")
                if len(cand) > 1:
                    raise Bad(f"{at or 'base'} branches to {', '.join(cand)}; name one")
                at = cand[0]
            return [at]
        r = self.g.resolve(spec)
        if r is None:
            raise Bad(f"cannot {what} to base")
        return [r]

    def upgrade(self, spec):
        need = self.g.by_pos(self.g.ancestors(self.targets(spec, "upgrade")) - self.applied)
        if not need:
            say("  nothing to upgrade")
            return
        for r in need:
            x = self.g.revs[r]
            bad = run_steps(self.schema, x["up"])
            if bad:
                say(f"  failed {r} at step {bad[0]} ({bad[1]}): {bad[2]}; rolled back")
                return
            self.applied.add(r)
            say(f"  upgrade {self.from_text(r)} -> {r}, {x['message']}")

    def downgrade(self, spec):
        if spec == "base":
            gone = set(self.applied)
        elif spec.startswith("-") and spec[1:].isdigit() and int(spec[1:]) > 0:
            left = set(self.applied)
            for _ in range(int(spec[1:])):
                cur = self.g.current(left)
                if not cur:
                    raise Bad(f"relative revision {spec} goes past base")
                if len(cur) > 1:
                    raise Bad("multiple current heads; name a target")
                left.discard(cur[0])
            gone = self.applied - left
        else:
            r = self.g.resolve(spec)
            if r is None:
                gone = set(self.applied)
            else:
                if r not in self.applied:
                    raise Bad(f"revision {r} is not applied")
                gone = self.g.descendants(r) & self.applied
        if not gone:
            say("  nothing to downgrade")
            return
        for r in self.g.by_pos(gone, rev=True):
            x = self.g.revs[r]
            bad = run_steps(self.schema, x["dn"])
            if bad:
                say(f"  failed {r} at step {bad[0]} ({bad[1]}): {bad[2]}; rolled back")
                return
            self.applied.discard(r)
            say(f"  downgrade {r} -> {self.from_text(r)}, {x['message']}")

    def sql(self, spec):
        need = self.g.by_pos(self.g.ancestors(self.targets(spec, "upgrade")) - self.applied)
        if not need:
            say("  nothing to upgrade")
            return
        sc = copy_schema(self.schema)
        applied = set(self.applied)
        say("  BEGIN;")
        if not applied:
            say("  CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL, PRIMARY KEY (version_num));")
        for r in need:
            x = self.g.revs[r]
            say(f"  -- upgrade {self.from_text(r)} -> {r}, {x['message']}")
            bad = run_steps(sc, x["up"])
            if bad:
                say(f"  -- failed {r} at step {bad[0]} ({bad[1]}): {bad[2]}")
                say("  ROLLBACK;")
                return
            for o in x["up"]:
                for s in op_sql(o):
                    say("  " + s)
            cur = self.g.current(applied)
            ps = [p for p in self.g.revs[r]["down"] if p in cur]
            ps = self.g.by_pos(ps)
            if not ps:
                say(f"  INSERT INTO alembic_version (version_num) VALUES ('{r}');")
            else:
                say(f"  UPDATE alembic_version SET version_num='{r}' WHERE version_num = '{ps[0]}';")
                for p in ps[1:]:
                    say(f"  DELETE FROM alembic_version WHERE version_num = '{p}';")
            applied.add(r)
        say("  COMMIT;")

    def stamp(self, spec):
        if spec == "heads":
            ts = list(self.g.heads)
        else:
            r = self.g.resolve(spec)
            ts = [] if r is None else [r]
        self.applied = self.g.ancestors(ts)
        say(f"  stamped {self.cur_text()}")

    def check(self):
        sc = {"tables": {}, "indexes": {}}
        for r in self.g.by_pos(self.applied):
            bad = run_steps(sc, self.g.revs[r]["up"])
            if bad:
                say(f"  replay fails at {r} step {bad[0]} ({bad[1]}): {bad[2]}")
                return
        want = schema_lines(sc)
        have = schema_lines(self.schema)
        if want == have:
            say("  schema matches")
            return
        say("  schema differs")
        for l in sorted(set(want) - set(have)):
            say(f"    missing: {l}")
        for l in sorted(set(have) - set(want)):
            say(f"    extra: {l}")

    def generate(self, label, parents, message):
        key = message + "|" + ",".join(parents)
        h = 0x811c9dc5
        for b in key.encode("utf-8"):
            h ^= b
            h = (h * 0x01000193) & 0xffffffff
        rid = f"{h:08x}"
        if rid in self.g.revs:
            raise Bad(f"revision {rid} already exists")
        slug = []
        for c in message.lower():
            ch = c if (c.isascii() and (c.islower() or c.isdigit())) else "_"
            if ch == "_" and slug and slug[-1] == "_":
                continue
            slug.append(ch)
        slug = "".join(slug).strip("_")[:24].rstrip("_")
        name = f"{rid}_{slug}.mig"
        lines = ["# generated by mini_alembic", f"revision: {rid}",
                 f"down: {', '.join(parents) if parents else 'none'}"]
        if label:
            lines.append(f"label: {label}")
        lines += [f"message: {message}", "", "upgrade:", "downgrade:"]
        os.makedirs("data/out/versions", exist_ok=True)
        with open(f"data/out/versions/{name}", "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(lines) + "\n")
        with open(f"data/out/versions/{name}", encoding="utf-8", newline="") as fh:
            r = parse_mig(f"out/versions/{name}", fh.read())
        if isinstance(r, str):
            raise Bad(r)
        revs = list(self.g.revs.values()) + [r]
        self.g = Graph(revs)
        say(f"  generated out/versions/{name}")

    def show(self, spec):
        r = self.g.resolve(spec)
        if r is None:
            raise Bad("base is not a revision")
        x = self.g.revs[r]
        say(f"  revision: {r}" + (" (head)" if r in self.g.heads else ""))
        say(f"  file: {x['path']}")
        if x["label"]:
            say(f"  label: {x['label']}")
        say(f"  message: {x['message']}")
        say(f"  down: {self.from_text(r)}")
        ch = self.g.children[r]
        say(f"  children: {', '.join(ch) if ch else 'none'}")
        for name, ops in (("upgrade", x["up"]), ("downgrade", x["dn"])):
            n = len(ops)
            say(f"  {name}: " + ("no steps" if n == 0 else f"{n} step" + ("" if n == 1 else "s")))
            for o in ops:
                say(f"    {o['text']}")

    def history(self):
        for r in reversed(self.g.order):
            x = self.g.revs[r]
            tags = ""
            if x["label"]:
                tags += f" ({x['label']})"
            if r in self.g.heads:
                tags += " (head)"
            if len(self.g.children[r]) > 1:
                tags += " (branchpoint)"
            if len(x["down"]) > 1:
                tags += " (mergepoint)"
            if r in self.g.current(self.applied):
                tags += " (current)"
            say(f"  {self.from_text(r)} -> {r}{tags}, {x['message']}")


def one_arg(cmd, args):
    if not args:
        raise Bad(f"{cmd} needs a target")
    if len(args) > 1:
        raise Bad(f"{cmd} takes one target")
    return args[0]


def main():
    if os.path.exists("data/out"):
        shutil.rmtree("data/out")
    os.makedirs("data/out")
    env = Env(load_revisions(True))
    with open("data/script.txt", encoding="utf-8", newline="") as fh:
        script = fh.read().split("\n")
    count = 0
    for line in script:
        s = line.strip()
        if s == "" or s.startswith("#"):
            continue
        count += 1
        say(f"> {s}")
        w = s.split()
        cmd, args = w[0], w[1:]
        try:
            if cmd == "current":
                say(f"  current: {env.cur_text()}")
            elif cmd == "heads":
                say("  heads: " + ", ".join(
                    h + (f" ({env.g.revs[h]['label']})" if env.g.revs[h]["label"] else "")
                    for h in env.g.heads))
            elif cmd == "history":
                env.history()
            elif cmd == "upgrade":
                env.upgrade(one_arg(cmd, args))
            elif cmd == "downgrade":
                env.downgrade(one_arg(cmd, args))
            elif cmd == "sql":
                env.sql(one_arg(cmd, args))
            elif cmd == "stamp":
                env.stamp(one_arg(cmd, args))
            elif cmd == "check":
                env.check()
            elif cmd == "schema":
                lines = schema_lines(env.schema)
                for l in lines or ["(no tables)"]:
                    say("  " + l)
            elif cmd == "show":
                env.show(one_arg(cmd, args))
            elif cmd == "revision":
                if len(args) < 3:
                    raise Bad("usage: revision <label|-> <parent> <message>")
                label = None if args[0] == "-" else args[0]
                if label is not None:
                    if not is_label(label):
                        raise Bad(f"bad label '{label}'")
                    if label in env.g.labels:
                        raise Bad(f"label {label} already used by {env.g.labels[label]}")
                p = env.g.resolve(args[1])
                env.generate(label, [] if p is None else [p], " ".join(args[2:]))
            elif cmd == "merge":
                if not args:
                    raise Bad("merge needs a message")
                if len(env.g.heads) < 2:
                    raise Bad("nothing to merge: one head")
                env.generate(None, list(env.g.heads), " ".join(args))
            elif cmd == "restart":
                env.save()
                env = Env(load_revisions(False))
                env.restore()
                say(f"  restarted at {env.cur_text()}, {len(env.schema['tables'])} tables, "
                    f"{len(env.schema['indexes'])} indexes")
            else:
                raise Bad(f"unknown command '{cmd}'")
        except Bad as e:
            say(f"  error: {e}")
        env.save()
    say(f"ran {count} commands")
    print("\n".join(OUT))


main()
