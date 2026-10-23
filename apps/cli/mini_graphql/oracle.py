"""Run data/jobs.txt against the vendored graphql-core 3.2.6 and print the
results: expected.out.

Run: python3 -I -B oracle.py > expected.out
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from graphql import (  # noqa: E402
    GraphQLError,
    Source,
    parse,
    parse_const_value,
    parse_type,
    parse_value,
    print_ast,
    version,
)
from graphql.language import Lexer, TokenKind  # noqa: E402
from graphql.language import ast as gast  # noqa: E402
from graphql.language.location import SourceLocation  # noqa: E402

assert version == "3.2.6"
DATA = os.path.join(HERE, "data")


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8", newline="") as f:
        return f.read()


def emit(text, indent="  "):
    for line in text.split("\n"):
        print(indent + "|" + (" " + line if line else ""))


def show_error(e, indent="  "):
    print(indent + "error " + type(e).__name__)
    try:
        text = str(e)
    except Exception as inner:  # print_location can fail on its own
        text = e.message + "\n\n(str() raised %s: %s)" % (type(inner).__name__, inner)
    emit(text, indent)


def first_location(e):
    if isinstance(e, GraphQLError) and e.locations:
        loc = e.locations[0]
        return "%d:%d" % (loc.line, loc.column)
    return "?"


# ------------------------------------------------------------ jobs

def job_parse(rel, opts):
    kw = {}
    for o in opts:
        if o == "no_location":
            kw["no_location"] = True
        elif o == "legacy":
            kw["allow_legacy_fragment_variables"] = True
        elif o.startswith("max_tokens="):
            kw["max_tokens"] = int(o.split("=")[1])
    try:
        doc = parse(Source(read(rel), rel), **kw)
    except Exception as e:
        show_error(e)
        return
    emit(print_ast(doc))


def job_value(rel, fn):
    try:
        node = fn(Source(read(rel)))
    except Exception as e:
        show_error(e)
        return
    emit(print_ast(node))


def job_tokens(rel):
    lexer = Lexer(Source(read(rel), rel))
    first = lexer.token
    err = None
    try:
        while lexer.advance().kind != TokenKind.EOF:
            pass
    except Exception as e:
        err = e
    t = first
    while t is not None:
        print("  " + repr(t))
        t = t.next
    if err is not None:
        show_error(err)


# ------------------------------------------------------------ programs

def fmt(files):
    for rel in files:
        body = read(rel)
        try:
            doc = parse(Source(body, rel))
        except GraphQLError as e:
            print("  %s: error at %s" % (rel, first_location(e)))
            show_error(e, "    ")
            continue
        printed = print_ast(doc)
        if body == printed + "\n":
            print("  %s: ok" % rel)
        else:
            print("  %s: would reformat (%d lines -> %d lines)"
                  % (rel, body.count("\n"), printed.count("\n") + 1))
            emit(printed, "    ")


def selections_of(node):
    ss = getattr(node, "selection_set", None)
    return ss.selections if ss is not None else []


def spreads(node, frags, seen, missing):
    for s in selections_of(node):
        if isinstance(s, gast.FragmentSpreadNode):
            name = s.name.value
            if name in seen:
                continue
            seen.add(name)
            if name in frags:
                spreads(frags[name], frags, seen, missing)
            else:
                missing.add(name)
        else:
            spreads(s, frags, seen, missing)


def depth(node, frags, stack):
    best = 0
    for s in selections_of(node):
        if isinstance(s, gast.FieldNode):
            d = 1 + (depth(s, frags, stack) if s.selection_set else 0)
        elif isinstance(s, gast.InlineFragmentNode):
            d = depth(s, frags, stack)
        else:
            name = s.name.value
            if name in frags and name not in stack:
                d = depth(frags[name], frags, stack + [name])
            else:
                d = 0
        best = max(best, d)
    return best


def root_fields(node, frags, out, stack):
    for s in selections_of(node):
        if isinstance(s, gast.FieldNode):
            name = (s.alias or s.name).value
            if name not in out:
                out.append(name)
        elif isinstance(s, gast.InlineFragmentNode):
            root_fields(s, frags, out, stack)
        else:
            name = s.name.value
            if name in frags and name not in stack:
                root_fields(frags[name], frags, out, stack + [name])


def fnv1a(text):
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) % (1 << 32)
    return "%08x" % h


def manifest(files):
    docs = []
    frags = {}
    for rel in files:
        try:
            doc = parse(Source(read(rel), rel))
        except GraphQLError as e:
            print("  %s: skipped, %s at %s" % (rel, e.message, first_location(e)))
            continue
        docs.append((rel, doc))
        for d in doc.definitions:
            if isinstance(d, gast.FragmentDefinitionNode):
                if d.name.value in frags:
                    print("  %s: fragment %s defined twice" % (rel, d.name.value))
                else:
                    frags[d.name.value] = d
    names = set()
    count = 0
    for rel, doc in docs:
        for d in doc.definitions:
            if not isinstance(d, gast.OperationDefinitionNode):
                continue
            count += 1
            name = d.name.value if d.name else "(anonymous)"
            print("  %s %s  [%s]" % (d.operation.value, name, rel))
            if d.name and name in names:
                print("    duplicate operation name")
            names.add(name)
            vars_ = [print_ast(v) for v in d.variable_definitions]
            print("    variables: " + (", ".join(vars_) if vars_ else "none"))
            seen, missing = set(), set()
            spreads(d, frags, seen, missing)
            used = sorted(seen - missing)
            print("    fragments: " + (", ".join(used) if used else "none"))
            if missing:
                print("    missing fragments: " + ", ".join(sorted(missing)))
            fields = []
            root_fields(d, frags, fields, [])
            print("    root fields: " + ", ".join(fields))
            print("    depth: %d" % depth(d, frags, []))
            text = "\n\n".join([print_ast(d)] + [print_ast(frags[n]) for n in used])
            print("    document: %d characters, id %s" % (len(text), fnv1a(text)))
    print("  %d operations, %d fragments" % (count, len(frags)))


BUILTIN_SCALARS = {"Int", "Float", "String", "Boolean", "ID"}
BUILTIN_DIRECTIVES = {"skip", "include", "deprecated", "specifiedBy"}

TYPE_KINDS = {
    gast.ScalarTypeDefinitionNode: "scalar",
    gast.ObjectTypeDefinitionNode: "type",
    gast.InterfaceTypeDefinitionNode: "interface",
    gast.UnionTypeDefinitionNode: "union",
    gast.EnumTypeDefinitionNode: "enum",
    gast.InputObjectTypeDefinitionNode: "input",
}
EXT_KINDS = {
    gast.ScalarTypeExtensionNode: "scalar",
    gast.ObjectTypeExtensionNode: "type",
    gast.InterfaceTypeExtensionNode: "interface",
    gast.UnionTypeExtensionNode: "union",
    gast.EnumTypeExtensionNode: "enum",
    gast.InputObjectTypeExtensionNode: "input",
}


def where(rel, node):
    loc = node.loc.source.get_location(node.loc.start)
    return "%s:%d:%d" % (rel, loc.line, loc.column)


def named(t):
    while not isinstance(t, gast.NamedTypeNode):
        t = t.type
    return t


def schema(files):
    types = {}
    order = []
    directives = []
    ops = []
    refs = []
    dir_uses = []

    def uses(rel, node):
        for dn in node.directives or []:
            dir_uses.append((dn.name.value, where(rel, dn)))

    def members(t, node):
        for f in getattr(node, "fields", None) or []:
            t["members"].append(f.name.value)
        for v in getattr(node, "values", None) or []:
            t["members"].append(v.name.value)
        for m in getattr(node, "types", None) or []:
            t["members"].append(m.name.value)
        for i in getattr(node, "interfaces", None) or []:
            t["interfaces"].append(i.name.value)

    def refs_of(rel, node):
        for i in getattr(node, "interfaces", None) or []:
            refs.append((i.name.value, where(rel, i)))
        for m in getattr(node, "types", None) or []:
            refs.append((m.name.value, where(rel, m)))
        for f in getattr(node, "fields", None) or []:
            nt = named(f.type)
            refs.append((nt.name.value, where(rel, nt)))
            uses(rel, f)
            for a in getattr(f, "arguments", None) or []:
                nt = named(a.type)
                refs.append((nt.name.value, where(rel, nt)))
                uses(rel, a)
        for v in getattr(node, "values", None) or []:
            uses(rel, v)
        uses(rel, node)

    for rel in files:
        try:
            doc = parse(Source(read(rel), rel))
        except GraphQLError as e:
            print("  %s: skipped, %s at %s" % (rel, e.message, first_location(e)))
            continue
        for d in doc.definitions:
            kind = TYPE_KINDS.get(type(d))
            if kind:
                name = d.name.value
                if name in types:
                    print("  %s: %s %s defined again" % (where(rel, d), kind, name))
                    continue
                types[name] = {"kind": kind, "members": [], "interfaces": [], "ext": 0}
                order.append(name)
                members(types[name], d)
                refs_of(rel, d)
                continue
            kind = EXT_KINDS.get(type(d))
            if kind:
                name = d.name.value
                t = types.get(name)
                if t is None:
                    print("  %s: extend %s %s, which is not defined" % (where(rel, d), kind, name))
                elif t["kind"] != kind:
                    print("  %s: extend %s %s, which is a %s" % (where(rel, d), kind, name, t["kind"]))
                else:
                    t["ext"] += 1
                    members(t, d)
                refs_of(rel, d)
                continue
            if isinstance(d, (gast.SchemaDefinitionNode, gast.SchemaExtensionNode)):
                for o in d.operation_types:
                    ops.append("%s %s" % (o.operation.value, o.type.name.value))
                    refs.append((o.type.name.value, where(rel, o.type)))
                uses(rel, d)
            elif isinstance(d, gast.DirectiveDefinitionNode):
                args = [a.name.value for a in d.arguments]
                directives.append("@%s(%s)%s on %s" % (
                    d.name.value, ", ".join(args), " repeatable" if d.repeatable else "",
                    " | ".join(n.value for n in d.locations)))
                for a in d.arguments:
                    nt = named(a.type)
                    refs.append((nt.name.value, where(rel, nt)))
                    uses(rel, a)
            else:
                print("  %s: %s is not a type system definition" % (where(rel, d), type(d).__name__))
    print("  schema: " + (", ".join(ops) if ops else "none"))
    for name in sorted(order):
        t = types[name]
        head = "%s %s" % (t["kind"], name)
        if t["interfaces"]:
            head += " implements " + " & ".join(t["interfaces"])
        sep = " = " if t["kind"] == "union" else ": "
        body = (" | " if t["kind"] == "union" else ", ").join(t["members"])
        line = head + (sep + body if body else "")
        if t["ext"]:
            line += " (+%d extension%s)" % (t["ext"], "" if t["ext"] == 1 else "s")
        print("  " + line)
    for d in directives:
        print("  directive " + d)
    defined = set(types) | BUILTIN_SCALARS
    shown = set()
    for name, at in refs:
        if name not in defined and name not in shown:
            shown.add(name)
            print("  unknown type %s, first at %s" % (name, at))
    known = {d.split("(")[0][1:] for d in directives} | BUILTIN_DIRECTIVES
    shown = set()
    for name, at in dir_uses:
        if name not in known and name not in shown:
            shown.add(name)
            print("  unknown directive @%s, first at %s" % (name, at))


def extract(files):
    for rel in files:
        text = read(rel)
        pos = 0
        while True:
            k = text.find("gql`", pos)
            if k < 0:
                break
            start = k + 4
            end = text.find("`", start)
            if end < 0:
                print("  %s: unterminated template" % rel)
                break
            pos = end + 1
            before = text[:start]
            line = before.count("\n") + 1
            col = start - (before.rfind("\n") + 1) + 1
            body = text[start:end]
            at = "%s:%d:%d" % (rel, line, col)
            if "${" in body:
                print("  %s: skipped, the template interpolates" % at)
                continue
            try:
                doc = parse(Source(body, rel, SourceLocation(line, col)))
            except GraphQLError as e:
                print("  %s: error" % at)
                show_error(e, "    ")
                continue
            defs = []
            for d in doc.definitions:
                if isinstance(d, gast.OperationDefinitionNode):
                    defs.append("%s %s" % (d.operation.value, d.name.value if d.name else "(anonymous)"))
                elif isinstance(d, gast.FragmentDefinitionNode):
                    defs.append("fragment %s on %s" % (d.name.value, d.type_condition.name.value))
            print("  %s: %s" % (at, ", ".join(defs)))


def main():
    for line in read("jobs.txt").split("\n"):
        if not line:
            continue
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line)
        parts = line.split(" ")
        cmd, args = parts[0], parts[1:]
        if cmd == "parse":
            job_parse(args[0], args[1:])
        elif cmd == "value":
            job_value(args[0], parse_value)
        elif cmd == "const_value":
            job_value(args[0], parse_const_value)
        elif cmd == "type":
            job_value(args[0], parse_type)
        elif cmd == "tokens":
            job_tokens(args[0])
        elif cmd == "!format":
            fmt(args)
        elif cmd == "!manifest":
            manifest(args)
        elif cmd == "!schema":
            schema(args)
        elif cmd == "!extract":
            extract(args)
        else:
            raise SystemExit("unknown job " + line)


main()
