#!/usr/bin/env python3
"""The oracle: reads the .proto files with a small parser (the mirror of
mini_protobuf's), builds descriptors from them, and runs data/jobs.tsv
with the real protobuf library (text_format, json_format and the upb
wire codec). Prints expected.out. Run mk.py first."""
import re

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from google.protobuf import json_format, text_format

F = descriptor_pb2.FieldDescriptorProto
SCALARS = {
    "double": F.TYPE_DOUBLE, "float": F.TYPE_FLOAT, "int64": F.TYPE_INT64,
    "uint64": F.TYPE_UINT64, "int32": F.TYPE_INT32, "fixed64": F.TYPE_FIXED64,
    "fixed32": F.TYPE_FIXED32, "bool": F.TYPE_BOOL, "string": F.TYPE_STRING,
    "bytes": F.TYPE_BYTES, "uint32": F.TYPE_UINT32, "sfixed32": F.TYPE_SFIXED32,
    "sfixed64": F.TYPE_SFIXED64, "sint32": F.TYPE_SINT32, "sint64": F.TYPE_SINT64,
}
LABELS = {"optional": F.LABEL_OPTIONAL, "required": F.LABEL_REQUIRED,
          "repeated": F.LABEL_REPEATED}

TOKEN = re.compile(r'\s+|//[^\n]*|/\*.*?\*/|([A-Za-z_][A-Za-z0-9_.]*)|'
                   r'(-?[0-9][0-9A-Za-z_.+-]*)|("(?:[^"\\]|\\.)*")|(.)', re.S)


def tokens(text):
    out = []
    for m in TOKEN.finditer(text):
        tok = m.group(1) or m.group(2) or m.group(3) or m.group(4)
        if tok:
            out.append(tok)
    return out


class Proto:
    """A recursive-descent reader for the proto2/proto3 subset the files
    use: package, options, messages, enums, oneofs, maps, reserved."""

    def __init__(self, name, text):
        self.t = tokens(text)
        self.i = 0
        self.fdp = descriptor_pb2.FileDescriptorProto(name=name)
        self.fields = []  # (field proto, type name, scope)

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else ""

    def next(self):
        tok = self.peek()
        self.i += 1
        return tok

    def expect(self, tok):
        got = self.next()
        assert got == tok, (tok, got, self.i)

    def constant(self):
        tok = self.next()
        if tok.startswith('"'):
            return tok[1:-1]
        return tok

    def parse(self):
        self.fdp.syntax = "proto2"
        while self.peek():
            tok = self.next()
            if tok == "syntax":
                self.expect("=")
                self.fdp.syntax = self.constant()
                self.expect(";")
            elif tok == "package":
                self.fdp.package = self.next()
                self.expect(";")
            elif tok == "option":
                while self.next() != ";":
                    pass
            elif tok == "message":
                self.message(self.fdp.message_type.add(), self.prefix())
            elif tok == "enum":
                self.enum(self.fdp.enum_type.add())
        self.resolve()
        return self.fdp

    def prefix(self):
        return "." + self.fdp.package if self.fdp.package else ""

    def options(self):
        opts = {}
        if self.peek() == "[":
            self.next()
            while True:
                key = self.next()
                self.expect("=")
                opts[key] = self.constant()
                if self.next() == "]":
                    break
        return opts

    def enum(self, e):
        e.name = self.next()
        self.expect("{")
        while self.peek() != "}":
            name = self.next()
            if name == "option":
                while self.next() != ";":
                    pass
                continue
            self.expect("=")
            v = e.value.add(name=name, number=int(self.next()))
            self.options()
            self.expect(";")
        self.next()

    def message(self, m, scope):
        m.name = self.next()
        scope = scope + "." + m.name
        self.expect("{")
        synthetic = []
        while self.peek() != "}":
            tok = self.peek()
            if tok == "message":
                self.next()
                self.message(m.nested_type.add(), scope)
            elif tok == "enum":
                self.next()
                self.enum(m.enum_type.add())
            elif tok == "reserved":
                while self.next() != ";":
                    pass
            elif tok == "option":
                while self.next() != ";":
                    pass
            elif tok == "oneof":
                self.next()
                index = len(m.oneof_decl)
                m.oneof_decl.add(name=self.next())
                self.expect("{")
                while self.peek() != "}":
                    f = self.field(m, scope, None)
                    f.oneof_index = index
                self.next()
            elif tok == "map":
                self.next()
                self.expect("<")
                key = self.next()
                self.expect(",")
                val = self.next()
                self.expect(">")
                name = self.next()
                self.expect("=")
                number = int(self.next())
                self.options()
                self.expect(";")
                entry = m.nested_type.add(name="".join(
                    p[:1].upper() + p[1:] for p in name.split("_")) + "Entry")
                entry.options.map_entry = True
                kf = entry.field.add(name="key", number=1, label=F.LABEL_OPTIONAL)
                self.typed(kf, key, scope + "." + entry.name)
                vf = entry.field.add(name="value", number=2, label=F.LABEL_OPTIONAL)
                self.typed(vf, val, scope + "." + entry.name)
                f = m.field.add(name=name, number=number, label=F.LABEL_REPEATED)
                self.typed(f, scope + "." + entry.name, scope)
            else:
                f = self.field(m, scope, synthetic)
        self.next()
        for f in synthetic:
            f.oneof_index = len(m.oneof_decl)
            m.oneof_decl.add(name="_" + f.name)

    def field(self, m, scope, synthetic):
        label = F.LABEL_OPTIONAL
        explicit = False
        if self.peek() in LABELS:
            label = LABELS[self.next()]
            explicit = True
        typ = self.next()
        f = m.field.add(name=self.next(), label=label)
        self.expect("=")
        f.number = int(self.next())
        opts = self.options()
        self.expect(";")
        self.typed(f, typ, scope)
        if "default" in opts:
            f.default_value = opts["default"]
        if "json_name" in opts:
            f.json_name = opts["json_name"]
        if opts.get("packed") == "true":
            f.options.packed = True
        if (self.fdp.syntax == "proto3" and explicit and label == F.LABEL_OPTIONAL
                and synthetic is not None):
            f.proto3_optional = True
            synthetic.append(f)
        return f

    def typed(self, f, typ, scope):
        if typ in SCALARS:
            f.type = SCALARS[typ]
        else:
            self.fields.append((f, typ, scope))

    def symbols(self):
        out = {}

        def walk(prefix, msgs, enums):
            for e in enums:
                out[prefix + "." + e.name] = F.TYPE_ENUM
            for m in msgs:
                out[prefix + "." + m.name] = F.TYPE_MESSAGE
                walk(prefix + "." + m.name, m.nested_type, m.enum_type)
        walk(self.prefix(), self.fdp.message_type, self.fdp.enum_type)
        return out

    def resolve(self):
        syms = self.symbols()
        for f, typ, scope in self.fields:
            if typ.startswith("."):
                full = typ
            else:
                first = typ.split(".")[0]
                full = None
                s = scope
                while True:
                    if s + "." + first in syms or any(
                            k.startswith(s + "." + first + ".") for k in syms):
                        full = s + "." + typ
                        break
                    if not s:
                        break
                    s = s[:s.rindex(".")] if "." in s else ""
            f.type = syms[full]
            f.type_name = full


POOL = descriptor_pool.DescriptorPool()
LOADED = set()


def load_proto(name):
    if name not in LOADED:
        with open("data/" + name) as f:
            POOL.Add(Proto(name, f.read()).parse())
        LOADED.add(name)


def message_class(proto, name):
    load_proto(proto)
    return message_factory.GetMessageClass(POOL.FindMessageTypeByName(name))


def read(path, mode="r"):
    with open("data/" + path, mode) as f:
        return f.read()


def hexdump(b):
    lines = ["  %d bytes" % len(b)]
    for i in range(0, len(b), 24):
        lines.append("    " + b[i:i + 24].hex(" "))
    return "\n".join(lines)


def indented(text):
    return "\n".join("  " + line for line in text.rstrip("\n").split("\n")) if text else "  (empty)"


def run(f):
    kind = f[0]
    if kind == "raw":
        cls = message_class("empty.proto", "empty.Empty")
        msg = cls.FromString(read(f[1], "rb"))
        return indented(text_format.MessageToString(msg, print_unknown_fields=True))
    cls = message_class(f[1], f[2])
    if kind == "encode":
        msg = text_format.Parse(read(f[3]), cls())
        return hexdump(msg.SerializeToString(deterministic=True))
    if kind == "text":
        msg = text_format.Parse(read(f[3]), cls())
        return indented(text_format.MessageToString(msg))
    if kind == "decode":
        msg = cls.FromString(read(f[3], "rb"))
        return indented(text_format.MessageToString(msg))
    if kind == "json":
        msg = cls.FromString(read(f[3], "rb"))
        opts = f[4:]
        return indented(json_format.MessageToJson(
            msg, sort_keys=True,
            preserving_proto_field_name="names" in opts,
            always_print_fields_with_no_presence="defaults" in opts,
            use_integers_for_enums="ints" in opts))
    if kind == "fromjson":
        msg = json_format.Parse(read(f[3]), cls())
        return indented(text_format.MessageToString(msg))
    if kind == "roundtrip":
        data = read(f[3], "rb")
        out = cls.FromString(data).SerializeToString(deterministic=True)
        if out == data:
            return "  same %d bytes" % len(out)
        return "  changed:\n" + hexdump(out)
    raise ValueError(kind)


def main():
    for job in read("jobs.tsv").split("\n")[:-1]:
        f = job.split("\t")
        print("== " + " ".join(f))
        try:
            print(run(f))
        except Exception as e:
            print("  %s: %s" % (type(e).__name__, e))


if __name__ == "__main__":
    main()
