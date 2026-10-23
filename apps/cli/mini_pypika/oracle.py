#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored PyPika and prints
what each step gives. A step is a Python expression over PyPika's API,
evaluated with eval() in an environment that persists until a "reset"
step; "let" binds names, "show" prints str() of the value, and an
exception prints as "error <class>: <message>". The three programs (a
schema migrator, a report compiler and a bulk loader) write SQL files
under data/out/ and print each file back after "  |".

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
from pypika import (  # noqa: E402
    NULL,
    SYSTEM_TIME,
    AliasedQuery,
    Array,
    Bracket,
    Case,
    ClickHouseQuery,
    Column,
    Columns,
    Criterion,
    CustomFunction,
    Database,
    DatePart,
    EmptyCriterion,
    Field,
    FormatParameter,
    Index,
    Interval,
    JoinType,
    MSSQLQuery,
    MySQLQuery,
    NamedParameter,
    Not,
    NullValue,
    NumericParameter,
    OracleQuery,
    Order,
    Parameter,
    PostgreSQLQuery,
    PyformatParameter,
    QmarkParameter,
    Query,
    RedshiftQuery,
    Rollup,
    Schema,
    SQLLiteQuery,
    Table,
    Tables,
    Tuple,
    VerticaQuery,
)
from pypika import analytics as an  # noqa: E402
from pypika import functions as fn  # noqa: E402
from pypika.dialects import SnowflakeQuery  # noqa: E402
from pypika.enums import ReferenceOption, SqlTypes  # noqa: E402
from pypika.terms import Values, ValueWrapper  # noqa: E402

DATA = os.path.join(HERE, "data")

BASE = {
    "NULL": NULL,
    "SYSTEM_TIME": SYSTEM_TIME,
    "AliasedQuery": AliasedQuery,
    "Array": Array,
    "Bracket": Bracket,
    "Case": Case,
    "ClickHouseQuery": ClickHouseQuery,
    "Column": Column,
    "Columns": Columns,
    "Criterion": Criterion,
    "CustomFunction": CustomFunction,
    "Database": Database,
    "DatePart": DatePart,
    "EmptyCriterion": EmptyCriterion,
    "Field": Field,
    "FormatParameter": FormatParameter,
    "Index": Index,
    "Interval": Interval,
    "JoinType": JoinType,
    "MSSQLQuery": MSSQLQuery,
    "MySQLQuery": MySQLQuery,
    "NamedParameter": NamedParameter,
    "Not": Not,
    "NullValue": NullValue,
    "NumericParameter": NumericParameter,
    "OracleQuery": OracleQuery,
    "Order": Order,
    "Parameter": Parameter,
    "PostgreSQLQuery": PostgreSQLQuery,
    "PyformatParameter": PyformatParameter,
    "QmarkParameter": QmarkParameter,
    "Query": Query,
    "RedshiftQuery": RedshiftQuery,
    "Rollup": Rollup,
    "Schema": Schema,
    "SQLLiteQuery": SQLLiteQuery,
    "SnowflakeQuery": SnowflakeQuery,
    "Table": Table,
    "Tables": Tables,
    "Tuple": Tuple,
    "Values": Values,
    "ValueWrapper": ValueWrapper,
    "VerticaQuery": VerticaQuery,
    "ReferenceOption": ReferenceOption,
    "SqlTypes": SqlTypes,
    "fn": fn,
    "an": an,
    "date": date,
}


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8") as f:
        return f.read()


def write_back(w, rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    lines = read(rel).split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    w("  wrote %s (%d lines)\n" % (rel, len(lines)))
    for ln in lines:
        w("  | %s\n" % ln)


def tsv(rel):
    rows = []
    for ln in read(rel).split("\n"):
        if ln and not ln.startswith("#"):
            rows.append(ln.split("\t"))
    return rows


# ------------------------------------------------------------ migrations

def value_of(text):
    """A default or a data value as the file spells it."""
    if text == "":
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    body = text[1:] if text.startswith("-") else text
    if body.isdigit():
        return int(text)
    if body.count(".") == 1 and body.replace(".", "").isdigit():
        return float(text)
    return text


def default_of(text):
    if text == "-":
        return None
    if text == "=now":
        return fn.Now()
    if text == "=curdate":
        return fn.CurDate()
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    return value_of(text)


MIGRATE_DIALECTS = [("ansi", Query), ("mysql", MySQLQuery), ("snowflake", SnowflakeQuery)]


def migrate(w, rel):
    rows = tsv(rel)
    order = []
    cols = {}
    for r in rows:
        if r[0] not in cols:
            order.append(r[0])
            cols[r[0]] = []
        cols[r[0]].append(r)
    for dname, cls in MIGRATE_DIALECTS:
        stmts = []
        for tname in order:
            q = cls.create_table(tname).if_not_exists()
            columns = []
            pks = []
            uniques = []
            unique_cols = {}
            fks = []
            fk_cols = {}
            for r in cols[tname]:
                nullable = {"yes": True, "no": False}.get(r[3])
                columns.append(Column(r[1], r[2], nullable=nullable, default=default_of(r[4])))
                for key in r[5].split(";"):
                    if key == "pk":
                        pks.append(r[1])
                    elif key.startswith("unique:"):
                        g = key[7:]
                        if g not in unique_cols:
                            uniques.append(g)
                            unique_cols[g] = []
                        unique_cols[g].append(r[1])
                    elif key.startswith("fk:"):
                        ref_t, ref_c = key[3:].split(".")
                        if ref_t not in fk_cols:
                            fks.append(ref_t)
                            fk_cols[ref_t] = ([], [])
                        fk_cols[ref_t][0].append(r[1])
                        fk_cols[ref_t][1].append(ref_c)
            q = q.columns(*columns)
            for g in uniques:
                q = q.unique(*unique_cols[g])
            if pks:
                q = q.primary_key(*pks)
            err = None
            for ref_t in fks:
                try:
                    q = q.foreign_key(
                        fk_cols[ref_t][0],
                        Table(ref_t),
                        fk_cols[ref_t][1],
                        on_delete=ReferenceOption.cascade,
                    )
                except Exception as e:
                    err = "-- %s: error %s: %s" % (tname, type(e).__name__, e)
            if err:
                stmts.append(err)
            stmts.append(str(q) + ";")
        for tname in reversed(order):
            stmts.append(str(cls.drop_table(tname).if_exists()) + ";")
        write_back(w, "out/migrate/%s.sql" % dname, "\n".join(stmts) + "\n")


# --------------------------------------------------------------- reports

FUNCS = {
    "sum": fn.Sum,
    "count": fn.Count,
    "avg": fn.Avg,
    "min": fn.Min,
    "max": fn.Max,
    "upper": fn.Upper,
    "lower": fn.Lower,
}


def ref(tok, tables):
    alias, name = tok.split(".")
    return tables[alias].field(name)


def term(tok, tables):
    if tok.endswith(")"):
        name, inner = tok[:-1].split("(", 1)
        if name == "distinct":
            return fn.Count(ref(inner, tables)).distinct()
        if inner == "*":
            return FUNCS[name]("*")
        return FUNCS[name](term(inner, tables))
    if "." in tok:
        return ref(tok, tables)
    return value_of(tok)


OPS = ["!=", ">=", "<=", "=", ">", "<"]


def condition(text, tables):
    alts = []
    for part in text.split(" or "):
        words = part.split(" ")
        if len(words) >= 2 and words[1] == "in":
            c = term(words[0], tables).isin([value_of(v) for v in words[2].split("|")])
        elif len(words) >= 2 and words[1] == "between":
            c = term(words[0], tables)[value_of(words[2]):value_of(words[3])]
        elif len(words) >= 2 and words[1] == "like":
            c = term(words[0], tables).like(words[2])
        elif len(words) >= 2 and words[1] == "isnull":
            c = term(words[0], tables).isnull()
        elif len(words) >= 2 and words[1] == "notnull":
            c = term(words[0], tables).notnull()
        else:
            for op in OPS:
                if op in part:
                    lhs, rhs = part.split(op, 1)
                    a = term(lhs, tables)
                    b = term(rhs, tables)
                    c = {
                        "!=": lambda: a != b,
                        ">=": lambda: a >= b,
                        "<=": lambda: a <= b,
                        "=": lambda: a == b,
                        ">": lambda: a > b,
                        "<": lambda: a < b,
                    }[op]()
                    break
        alts.append(c)
    out = alts[0]
    for c in alts[1:]:
        out = out | c
    return out


REPORT_DIALECTS = [
    ("ansi", Query),
    ("mysql", MySQLQuery),
    ("postgres", PostgreSQLQuery),
    ("mssql", MSSQLQuery),
    ("oracle", OracleQuery),
]


def build_report(cls, r):
    name, base, joins, select, where, group, having, order, limit, offset = r
    tables = {}
    tname, alias = base.split(":")
    tables[alias] = Table(tname).as_(alias)
    q = cls.from_(tables[alias])
    if joins != "-":
        for spec in joins.split(";"):
            how, jt, ja, rest = spec.split(" ", 3)
            tables[ja] = Table(jt).as_(ja)
            j = q.join(tables[ja], {"inner": JoinType.inner, "left": JoinType.left,
                                    "right": JoinType.right, "full": JoinType.full_outer}[how])
            if rest.startswith("using "):
                q = j.using(*rest[6:].split(","))
            else:
                lhs, rhs = rest.split("=")
                q = j.on(ref(lhs, tables) == ref(rhs, tables))
    selected = {}
    terms = []
    for item in select.split(","):
        if ":" in item:
            expr, al = item.split(":")
            t = term(expr, tables).as_(al)
            selected[al] = t
        else:
            t = term(item, tables)
        terms.append(t)
    q = q.select(*terms)
    if where != "-":
        for c in where.split(";"):
            q = q.where(condition(c, tables))
    if group != "-":
        q = q.groupby(*[term(g, tables) for g in group.split(",")])
    if having != "-":
        for c in having.split(";"):
            q = q.having(condition(c, tables))
    if order != "-":
        for item in order.split(","):
            key, direction = item.split(" ")
            t = selected[key] if key in selected else term(key, tables)
            q = q.orderby(t, order=Order.desc if direction == "desc" else Order.asc)
    if limit != "-":
        q = q.limit(int(limit))
    if offset != "-":
        q = q.offset(int(offset))
    return q


def report(w, rel):
    rows = tsv(rel)
    for dname, cls in REPORT_DIALECTS:
        out = []
        for r in rows:
            out.append("-- %s" % r[0])
            try:
                out.append(str(build_report(cls, r)) + ";")
            except Exception as e:
                out.append("-- error %s: %s" % (type(e).__name__, e))
        write_back(w, "out/reports/%s.sql" % dname, "\n".join(out) + "\n")


# ------------------------------------------------------------------ load

def csv_rows(rel):
    lines = [ln for ln in read(rel).split("\n") if ln]
    header = lines[0].split(",")
    return header, [[value_of(v) for v in ln.split(",")] for ln in lines[1:]]


def load(w, rel, tname, key, batch):
    header, rows = csv_rows(rel)
    t = Table(tname)
    others = [c for c in header if c != key]
    for dname in ("postgres", "mysql", "sqlite"):
        out = []
        for k in range(0, len(rows), batch):
            chunk = [tuple(r) for r in rows[k:k + batch]]
            if dname == "postgres":
                q = PostgreSQLQuery.into(t).columns(*header).insert(*chunk).on_conflict(key)
                for c in others:
                    q = q.do_update(c)
                q = q.returning(key)
            elif dname == "mysql":
                q = MySQLQuery.into(t).columns(*header).insert(*chunk)
                for c in others:
                    q = q.on_duplicate_key_update(t.field(c), Values(t.field(c)))
            else:
                q = SQLLiteQuery.into(t).columns(*header).insert_or_replace(*chunk)
            out.append(str(q) + ";")
        write_back(w, "out/load/%s.%s.sql" % (tname, dname), "\n".join(out) + "\n")


# ------------------------------------------------------------------ jobs

def run(w):
    env = dict(BASE)
    for ln in read("jobs.tsv").split("\n"):
        if not ln:
            continue
        kind, src = ln.split("\t", 1)
        if kind == "#":
            w("\n# %s\n" % src)
            continue
        if kind == "reset":
            env = dict(BASE)
            continue
        w("> %s\n" % src)
        try:
            if kind == "let":
                lhs, expr = src.split(" = ", 1)
                val = eval(expr, {"__builtins__": {}}, env)
                names = [n.strip() for n in lhs.split(",")]
                if len(names) == 1:
                    env[names[0]] = val
                else:
                    vals = list(val)
                    for n, v in zip(names, vals):
                        env[n] = v
            elif kind == "show":
                w("%s\n" % (eval(src, {"__builtins__": {}}, env),))
            elif kind == "program":
                args = src.split(" ")
                if args[0] == "migrate":
                    migrate(w, args[1])
                elif args[0] == "report":
                    report(w, args[1])
                elif args[0] == "load":
                    load(w, args[1], args[2], args[3], int(args[4]))
        except Exception as e:
            w("error %s: %s\n" % (type(e).__name__, e))


def main():
    out = []
    run(out.append)
    sys.stdout.write("".join(out))


main()
